# Production readiness, test matrix and troubleshooting

Source: **OFFICIAL XIAOMI** developer onboarding, design review, API, FAQ; recommendations labeled where applicable. Reviewed 2026-10-14.

## 1. Developer / application onboarding

1. Create or verify a Xiaomi developer account and register an application with its **package name** and signing certificate information.
2. In the developer console, enable **Super Island service** for the registered app. Enable **Push service** first if choosing the cloud MiPush route.
3. Submit the intended live-activity scenario for **pre-review**; avoid promotional advertising, loan offers, or unrelated engagement bait.
4. After pre-approval, submit the complete solution: use case, every transition node, first-render/auto-expand timing, compact big and small states, expanded Focus Notification, lock-screen/AOD states when relevant, UI mockups, and expiry rules.
5. After design approval, run integration/device testing. Xiaomi documents adding test devices by **OAID** via its authorized allowlist. Documented limit: **up to 10 devices per application** and **30-day allowlist validity**.
6. Add `<meta-data android:name="com.xiaomi.xms.APP_ID" android:value="@string/xiaomi_app_id" />` and a correct debug/release flag for signing-based authorization. `com.xiaomi.xms.BUILD_TYPE_DEBUG` is `true` for a test-signature debug build and `false` for release; release signing should match the registered production certificate.
7. Submit the tested **release APK** and reproducible scenario verification instructions for final production entitlement. Adding new island business scenes later requires a new submission and review.
8. Xiaomi documents staged rollout of first-time production approval, approximately **7-15 days** to full coverage. Treat this as platform guidance, not a guaranteed SLA.

Official source: https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2132

### Debug signing metadata (illustration)

```xml
<application>
    <meta-data
        android:name="com.xiaomi.xms.APP_ID"
        android:value="@string/xiaomi_app_id" />
    <meta-data
        android:name="com.xiaomi.xms.BUILD_TYPE_DEBUG"
        android:value="${isXiaomiDebugBuild}" />
</application>
```

Define `isXiaomiDebugBuild` for all variants with the appropriate build configuration. Do not commit production App Secret or private registration identifiers to shared samples. Do not confuse signing app ID metadata with Android's standard notification permission.

## 2. HyperOS 3 device and permission test matrix

Test at minimum:

| Device / environment | Expected outcome | Verify |
|---|---|---|
| Authorized Xiaomi/Redmi/POCO with **HyperOS 3**, Focus permission enabled | Valid approved island template | Small/big summary, expanded card, update, AOD if template supports |
| HyperOS 3 with **Focus permission disabled** | Normal fallback or filtered behavior based on app policy / `filterWhenNoPermission` | Never silently lose essential information |
| Other Android phone | Normal notification | Title, icon, body, click action, update/cancel |
| Android 13+ without `POST_NOTIFICATIONS` | No ordinary notification until user grants runtime permission | Explain necessity appropriately, don't repeatedly nag |
| Dark/light / large font / lock screen | Readable, privacy-safe | Text clipping, contrast, AOD and sensitive info |
| Network loss / dead app process | Local events delayed; approved MiPush still viable with connectivity | Recovery and expiry; no immortal stale status |
| Foldable / external display | Xiaomi standard templates manage layout adaptation | No clipping in supported variant |

## 3. Preflight checks

- JSON root is `param_v2`, and the payload is valid UTF-8 JSON with no JavaScript comments/trailing commas.
- `business` is a permitted scene identifier from your Xiaomi-approved application (not merely a plausible example string).
- `param_island.bigIslandArea` and `.smallIslandArea` exist and satisfy a specific supported Xiaomi template.
- `baseInfo`, `hintInfo`, progress, timer, text, action and images match the chosen expanded template; do not infer that any arbitrary combination will render.
- Byte size: `len(json.encode("utf-8")) <= 3072` (MiPush FAQ).
- Picture/action resource names referenced by JSON match `miui.focus.pics` / `miui.focus.actions` (local) or MiPush `miui.focus.pic_*` extras (server).
- Remote images are HTTPS, <=100 KB, valid ratio, and small count; local icons are square and sufficiently large.
- Android channel created, valid small icon, runtime permission requested, stable integer notification ID, content PendingIntent set.
- Same notification ID used on update. Server updates have order identity and strictly increasing `sequence`.
- Screen-reader, dark/light, reduced motion, large-font, lock-screen, background task expiry, and offline behaviors tested.
- Production manifest uses real registered APP_ID and correct debug flag; debug allowlist and approved business scene applied.

Run the shape-aware structural preflight: `python scripts/validate_payload.py examples/package-delivery.json --big-template 2 --small-template 1 --expanded-template 10 --picture miui.focus.pic_box --action miui.focus.action_track`.

## 4. Troubleshooting guide

| Symptom | Investigate | Resolution |
|---|---|---|
| Only normal notification appears | HyperOS 3 system protocol, service entitlement, approved scenario, focus toggle, notification permissions | Keep fallback and enable official approval/testing, verify the version-gate value is 3 and the approved scene code |
| Nothing appears | OS runtime `POST_NOTIFICATIONS`, channel settings, caller execution, `filterWhenNoPermission` | Ensure channel and runtime permissions; use normal notification for diagnostics |
| Island shows but text truncates | Compact A/B text too long, different typography/language | Shorten to one status/number, verify template and font size |
| Images missing | Mismatch of JSON key and `miui.focus.pics` icon key, wrong type, too-small bitmap | Match exact name and resource type; for MiPush, check HTTPS, size and aspect ratio |
| Buttons don't work | Missing Action `Bundle`, unsupported template, unsafe or unresolved `PendingIntent` | Provide explicit matching `Notification.Action`, secure PendingIntent, and test broadcast/activity |
| Updates appear as new items | Different ID/order key, invalid sequence, notification channel inconsistency | Reuse `notifyId`, keep order association, increment MiPush sequence |
| Island persists after task | No completion cancellation, confusing timeout units | Explicitly cancel; set separate island seconds and notification minutes |
| MiPush image download fails | HTTP, >100 KB, timeout, ratio, image count | Use reachable HTTPS image meeting restrictions |
| Community wrapper works only on some ROMs | Private hidden APIs, XMSF changes, R8/obfuscation, new OS build | Avoid binding product requirements to bypass mechanism; use official route |

## 5. Security, privacy and operational best practices

- Store all server credentials in a secrets manager; never package MiPush `APP_SECRET` inside an APK.
- Explicitly target Android receivers/activities and use immutable `PendingIntent`s unless mutability is required by the action; avoid exported components when not needed.
- Do not show sensitive names, full addresses, OTPs, or private details on always-on/lock-screen surfaces without appropriate user choice and privacy safeguards.
- Debounce high-frequency updates and use `.setOnlyAlertOnce(true)` for regular notification fallback; do not spam expansion via `enableFloat`.
- Prefer genuine time-sensitive service progress over advertising, push growth hacks, fake persistent status or continuous tracking unrelated to the active task.
- Establish a clear end state and cleanup across completion, error, user cancellation and logout.
- Test any community dependency's license, latest maintenance, transitive SDKs, privacy handling and proguard rules; pin a version and audit generated JSON.

References:
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2132
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2146
