#!/usr/bin/env python3
"""Sign the built APK with a configured keystore using Android SDK apksigner."""

import argparse
import os
from pathlib import Path
import subprocess


def find_default_apk(root: Path) -> tuple[Path, Path]:
    search_dirs = [
        root / "app/build/outputs/apk/normal/release",
        root / "app/build/outputs/apk/release",
        root / "app/build/outputs/apk/normal/debug",
        root / "app/build/outputs/apk/debug",
    ]
    for d in search_dirs:
        if d.is_dir():
            for candidate in sorted(d.glob("*.apk")):
                if not candidate.name.endswith("-signed.apk") and not candidate.name.endswith("-unaligned.apk"):
                    out_name = candidate.name.replace("-unsigned.apk", "-signed.apk") if candidate.name.endswith("-unsigned.apk") else candidate.stem + "-signed.apk"
                    return candidate, candidate.with_name(out_name)
    fallback = root / "app/build/outputs/apk/normal/release/app-release-unsigned.apk"
    return fallback, fallback.with_name("app-release-signed.apk")


def main():
    root = Path(__file__).resolve().parents[1]
    default_apk, default_out = find_default_apk(root)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apk", type=Path, default=default_apk, help="Path to input APK (default: %(default)s)")
    parser.add_argument("--out", type=Path, default=None, help="Path to output signed APK")
    parser.add_argument("--keystore", type=Path, default=None, help="Path to signing keystore")
    parser.add_argument("--ks-type", default=None, help="Keystore type (e.g. BKS, PKCS12, JKS)")
    parser.add_argument("--alias", default=None, help="Key alias")
    args = parser.parse_args()

    keystore_path = args.keystore or (Path(os.environ["SIGNING_KEYSTORE"]) if "SIGNING_KEYSTORE" in os.environ else None)
    if not keystore_path or not keystore_path.is_file():
        parser.error("Missing signing keystore; provide --keystore or set SIGNING_KEYSTORE.")
    if not args.apk.is_file():
        parser.error(f"Input APK not found: {args.apk}; build the app first.")

    key_alias = args.alias or os.environ.get("SIGNING_KEY_ALIAS")
    if not key_alias:
        parser.error("Key alias required; provide --alias or set SIGNING_KEY_ALIAS.")

    key_password = os.environ.get("SIGNING_KEY_PASSWORD")
    if key_password is None:
        parser.error("Key password required; set SIGNING_KEY_PASSWORD environment variable.")

    store_password = os.environ.get("SIGNING_STORE_PASSWORD", "")
    ks_type = (args.ks_type or os.environ.get("SIGNING_KEYSTORE_TYPE") or "BKS").upper()

    if args.out is None:
        out_name = args.apk.name.replace("-unsigned.apk", "-signed.apk") if args.apk.name.endswith("-unsigned.apk") else args.apk.stem + "-signed.apk"
        args.out = args.apk.with_name(out_name)

    if args.apk.resolve() == args.out.resolve():
        parser.error("Use a separate output path to preserve the input APK.")

    sdk = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
    if not sdk:
        properties = root / "local.properties"
        if properties.is_file():
            sdk = next((line.split("=", 1)[1] for line in properties.read_text().splitlines()
                        if line.startswith("sdk.dir=")), None)
    if not sdk:
        for standard_path in ["/usr/local/lib/android/sdk", Path.home() / "Android/Sdk", Path.home() / "Library/Android/sdk"]:
            if Path(standard_path).is_dir():
                sdk = str(standard_path)
                break
    if not sdk:
        parser.error("Set ANDROID_SDK_ROOT or sdk.dir in local.properties.")

    tools = [p for p in (Path(sdk) / "build-tools").glob("*/lib/apksigner.jar")
             if all(part.isdigit() for part in p.parents[1].name.split("."))]
    if not tools:
        parser.error("Android SDK apksigner.jar not found.")
    signer = max(tools, key=lambda p: tuple(map(int, p.parents[1].name.split("."))))

    cp_entries = [str(signer)]
    provider_args = []
    if ks_type == "BKS":
        cache = Path(os.environ.get("GRADLE_USER_HOME", Path.home() / ".gradle"))
        candidates = list((cache / "caches/modules-2/files-2.1/org.bouncycastle/bcprov-jdk18on").glob("*/*/*.jar"))
        if candidates:
            provider = max(candidates, key=lambda p: tuple(map(int, p.parents[1].name.split("."))))
        else:
            bc_cache = cache / "caches/bcprov-jdk18on-1.79.jar"
            if not bc_cache.is_file():
                import urllib.request
                bc_cache.parent.mkdir(parents=True, exist_ok=True)
                url = "https://repo1.maven.org/maven2/org/bouncycastle/bcprov-jdk18on/1.79/bcprov-jdk18on-1.79.jar"
                urllib.request.urlretrieve(url, bc_cache)
            provider = bc_cache
        cp_entries.append(str(provider))
        provider_args = ["--ks-provider-class", "org.bouncycastle.jce.provider.BouncyCastleProvider"]

    env = os.environ.copy()
    env["_SIGN_STORE_PASS"] = store_password
    env["_SIGN_KEY_PASS"] = key_password

    args.out.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "java", "-cp", os.pathsep.join(cp_entries),
        "com.android.apksigner.ApkSignerTool", "sign",
        "--ks", str(keystore_path),
        "--ks-type", ks_type,
        "--ks-key-alias", key_alias,
        "--ks-pass", "env:_SIGN_STORE_PASS",
        "--key-pass", "env:_SIGN_KEY_PASS",
    ] + provider_args + [
        "--out", str(args.out),
        str(args.apk)
    ]

    subprocess.run(command, env=env, check=True)
    subprocess.run(["java", "-jar", str(signer), "verify", "--verbose", str(args.out)], check=True)
    print(f"Successfully signed APK: {args.out}")


if __name__ == "__main__":
    main()
