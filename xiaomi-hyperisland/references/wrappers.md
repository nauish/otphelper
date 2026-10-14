# Library wrappers and third-party push adapters

**Research date: 2026-10-14.** These are **not** Xiaomi-maintained official API packages unless explicitly marked otherwise. Verify dependency availability, source, licenses, published releases, Android Gradle/SDK constraints, and device behavior before adopting.

## Comparison

| Option | Provenance | Best use | Caveats |
|---|---|---|---|
| Android `Notification` + `miui.focus.param` | **OFFICIAL XIAOMI integration contract** | Production app integrating authorized HyperIsland | Must handle JSON schema, assets, testing, and Xiaomi approval |
| MiPush Java Sender + `extra` | **OFFICIAL XIAOMI server path** | Remote progress when client process may be dead | Authorized MiPush/HyperIsland scene and `regId` sending required; credentials stay server-side |
| `hyperisland_kit:0.4.3` | **COMMUNITY Kotlin library** by D4vidDf | Type-safe builder, layouts, and local notification extras | Community release, not guaranteed by Xiaomi; still needs compatible device / approval |
| `Xiaomi-SuperIsland-Playground:v1` | **COMMUNITY SDK / EXPERIMENTAL XMSF methods** by HuberHaYu | Test playground and high-level publisher | HiddenApiBypass/XMSF internals, API 31+, fragility and policy/reliability risk; not an official exemption |
| Aliyun EMAS Xiaomi focus-push adapter | **THIRD-PARTY vendor API** | Existing Aliyun push infrastructure | Vendor-specific API parameters / limits; still requires Xiaomi-side permissions |
| JPush Xiaomi `mi_live_payload` adapter | **THIRD-PARTY vendor API** | Existing JPush infrastructure | Vendor-specific JSON nesting and routing; not raw MiPush SDK API |

## 1. HyperIsland ToolKit (community, Kotlin)

Website docs: https://hyperisland.d4viddf.com/docs/getting-started/  
Repository: https://github.com/D4vidDf/HyperIsland-ToolKit

The published getting-started guide advertises `io.github.d4viddf:hyperisland_kit:0.4.3` and **minSDK 24**. This is a *library compilation floor*, not a claim of HyperIsland rendering below HyperOS 3.

`app/build.gradle.kts`:

```kotlin
dependencies {
    implementation("io.github.d4viddf:hyperisland_kit:0.4.3")
}
```

Example use, based on the library's documented Builder API:

```kotlin
val hyper = HyperIslandNotification.Builder(context, "delivery", "Package update")
    .setBaseInfo(title = "Out for delivery", content = "Expected today")
    .addPicture(HyperPicture("box", context, R.drawable.ic_box))
    .setSmallIslandIcon("box")

if (HyperIslandNotification.isSupported(context)) {
    val extras = Bundle().apply {
        putString("miui.focus.param", hyper.buildJsonParam())
        putAll(hyper.buildResourceBundle())
    }
    val notification = Notification.Builder(context, CHANNEL_ID)
        .setSmallIcon(R.drawable.ic_notification)
        .setContentTitle("Out for delivery")
        .setContentText("Expected today")
        .addExtras(extras)
        .build()
    manager.notify(STABLE_ID, notification)
} else {
    // Post an ordinary Android notification through the same channel and ID.
}
```

Import Kotlin symbols according to the installed artifact and package version; the snippet assumes Android notification channel, permissions, and icon assets already exist. `isSupported()` is a convenience heuristic, **not** proof that an unapproved commercial scene is publishable. The library's own documentation refers to `setBaseInfo`, `addPicture`, `setSmallIslandIcon`, `buildJsonParam`, and `buildResourceBundle`. APIs may change: pin the actual version and run sample tests.

Also see:
- https://hyperisland.d4viddf.com/docs/builder/
- https://hyperisland.d4viddf.com/docs/components/island/big-island/

## 2. Xiaomi-SuperIsland-Playground SDK (community, experimental)

Repository: https://github.com/HuberHaYu/Xiaomi-SuperIsland-Playground

The project README documents Android **API 31+**, JDK **11+**, an Android sample app, and an embeddable `IslandClient` SDK that may use **HiddenApiBypass / XMSF**. Do not treat claims of working "without elevated privileges" as Xiaomi's formal production approval.

`settings.gradle.kts` repository setup (if not already configured):

```kotlin
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven(url = "https://jitpack.io")
    }
}
```

`app/build.gradle.kts`:

```kotlin
dependencies {
    implementation("com.github.HuberHaYu:Xiaomi-SuperIsland-Playground:v1")
}
```

README-documented entry point:

```kotlin
val island = IslandClient.get(this)
val draft = IslandDraftBuilder()
    .scene(IslandScene.GENERAL)
    .title("Delivery")
    .subtitle("Arriving soon")
    .source("Island")
    .progress(65)
    .build()

island.publish(draft) { outcome ->
    Log.d("Island", outcome.message)
}
// The README also names updateActive(...), cancel(notificationId), activeIslands.
```

Do not copy hidden APIs, patch XMSF, bypass permission checks, or rely on undocumented service spoofing as the default production implementation. Review user privacy, terms, maintenance, crash behavior, R8 rules, security surface, and library licensing before even evaluating such methods.

## 3. Aliyun EMAS / Alibaba Cloud Push (third-party server adapter)

English documentation: https://help.aliyun.com/en/document_detail/3037956.html

The vendor documents parameters such as:

- `AndroidXiaomiFocusParam` = the **JSON string** for `{"param_v2": {...}}`.
- `AndroidXiaomiFocusPics` = optional JSON string of `miui.focus.pic_*` -> HTTPS image URLs.
- Set Xiaomi-specific fallback notification fields as required by the Aliyun API.
- That provider's published parameter limits include **3072 bytes** for Focus Param and **1024 bytes** for the picture mapping string; treat these as vendor restrictions rather than assuming they are identical for raw MiPush.

**Pattern** (illustrative pseudocode, not a stand-alone executable Aliyun request):

```java
pushRequest.setAndroidXiaomiFocusParam(focusJsonString);
pushRequest.setAndroidXiaomiFocusPics(focusPicsJsonString);
// Set vendor-specific target, normal notification fallback and send parameters.
```

Only choose this adapter when the application uses Alibaba Cloud Push and has enabled compatible Xiaomi push services.

## 4. JPush / Jiguang Xiaomi live push (third-party server adapter)

English documentation: https://docs.jiguang.cn/en/jpush/server/push/rest_api_v3_push

JPush documents a Xiaomi-specific `third_party_channel.xiaomi.mi_live_payload` mapping containing `miui.focus.param`; note that some vendor endpoints accept **JSON objects** rather than raw JSON strings. Follow the vendor's actual API for the selected version.

Illustrative nesting (not a complete JPush request):

```json
{
  "third_party_channel": {
    "xiaomi": {
      "distribution": "ospush",
      "notify_id": 123456,
      "mi_live_payload": {
        "miui.focus.param": {
          "param_v2": {
            "business": "approved_scene",
            "param_island": {
              "bigIslandArea": {},
              "smallIslandArea": {}
            }
          }
        }
      }
    }
  }
}
```

As above, empty compact-area objects are **schema illustrations only**, not renderable template data. Check the official Xiaomi template library and JPush request schema before sending.

## Selection guidance

- Prefer the **official local** route for apps needing no server path and full production compliance.
- Prefer the **official MiPush** route for a task that must update after the app process is terminated.
- Consider the **D4vidDf Kotlin DSL** if reducing JSON/Bundle boilerplate is worth a maintained third-party dependency; audit its actual outputs against current Xiaomi templates.
- Keep the **HuberHaYu project** confined to exploration unless legal, security, stability, and Xiaomi service-authorization implications have been explicitly evaluated.
- Use **Aliyun or JPush** only when already committed to the respective push infrastructure; do not silently substitute one vendor's schema for another.
