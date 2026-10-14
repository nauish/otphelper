# Official Xiaomi HyperIsland API contract

Verified against Xiaomi HyperOS developer pages on **2026-10-14**. **Authority: OFFICIAL XIAOMI**, except where explicitly identified as an implementation recommendation.

## Contents

1. HyperOS 3 publication architecture
2. Envelope and core fields
3. Android publication and resource extras
4. MiPush publication and remote images
5. Capability / permission queries
6. Templates and known documentation pitfalls

## 1. HyperOS 3 publication architecture

- **HyperOS 3**: Xiaomi Super Island / HyperIsland (compact large/small island; expanded focus card; lock screen and AOD depending on templates).
- **Official local track**: build an Android notification and attach Xiaomi extras. Requires registration and approval for commercial production.
- **Official server track**: send through authorized MiPush, currently documented for `regId` targets, using the same JSON contract as client publication.
- **Separate system notification authorization** (`POST_NOTIFICATIONS` when required) from **Xiaomi scene, Focus Notification, and Super Island service authorization**.

**Key sources**:
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2141
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2132

## 2. Envelope and core fields

The local Android notification extra is the **serialized JSON string** under `miui.focus.param`.

```json
{
  "param_v2": {
    "protocol": 1,
    "business": "approved_business_scenario",
    "updatable": true,
    "islandFirstFloat": false,
    "enableFloat": false,
    "timeout": 30,
    "aodTitle": "Order in progress",
    "param_island": {
      "islandProperty": 1,
      "islandTimeout": 900,
      "bigIslandArea": {},
      "smallIslandArea": {}
    }
  }
}
```

**WARNING:** This is a **valid envelope illustration**, **not a complete renderable layout**. `{}` must be populated using an **approved template** for the chosen scene; expanded focus templates may also require `baseInfo`, `hintInfo`, other template components, and action assets. `protocol: 1` in Xiaomi's documented JSON example is **not** the same as `Settings.System.notification_focus_protocol == 3` (which detects the target OS).

### Top-level `param_v2` fields

| Key | Type | Scope / documented behavior |
|---|---|---|
| `business` | string | **Required** approved service/business scenario identifier; `taxi` appears in Xiaomi's sample. Do not invent a production-approved code. |
| `protocol` | number | `1` appears in Xiaomi's sample payload; it is distinct from the system version check (which must equal 3). Verify its meaning for the chosen approved template. |
| `updatable` | boolean | Long-running/updatable notification (`false` default). |
| `islandFirstFloat` | boolean | Expand automatically on first appearance; defaults `true`. Avoid overuse. |
| `enableFloat` | boolean | Auto-expand on update; defaults `false`. |
| `timeout` | integer | Overall notification timeout **minutes**; default `720`. `0` uses default according to FAQ. |
| `cancel` | boolean | On **MiPush**, `true` ends and clears focus notification / island. Client should call `NotificationManager.cancel`. |
| `reopen` | string | `reopen` or `close` after cancellation for same ID; documented prerequisite `updatable=true`. |
| `filterWhenNoPermission` | boolean | `false` (default) allows ordinary fallback; `true` filters notification if Focus Notification permission is disabled. |
| `orderId` | string | MiPush notification/order correlation. |
| `sequence` | long | Required for **MiPush real-time update scenarios**, monotonic per order to prevent out-of-order display. |
| `aodTitle`, `aodPic` | string | Always-on-display title and optional custom icon. |
| `baseInfo`, `hintInfo`, and other layout fields | objects | Template-specific expanded Focus Notification fields. Read official template library. |
| `param_island` | object | **Required** island data (see below). |

### Nested `param_v2.param_island`

| Key | Type | Scope / documented behavior |
|---|---|---|
| `islandProperty` | integer | `1` = information first; `2` = operations first; default `1`. |
| `islandOrder` | boolean | Whether updates change island sort order when summary hidden; default `false`. |
| `islandTimeout` | integer | Island lifetime in **seconds**; default **3600**. |
| `dismissIsland` | boolean | `true` ends compact island state. |
| `highlightColor` | string | Text emphasis color, validate contrast. |
| `bigIslandArea` | object | **Required** big summary island structure (chosen template's A and B regions). |
| `smallIslandArea` | object | **Required** small island structure. |
| `shareData` | object | Optional drag-share. When supported, prepare `pic`, `title`, `content`, `shareContent` per Xiaomi's documented schema. |

### Payload size and lifecycle

- Xiaomi FAQ states **`miui.focus.param` <= 3072 bytes** (UTF-8). Apply this proactively even to local builds as a safe portability check.
- Xiaomi's design defaults: expanded card automatically collapses after approximately **5 seconds**; without explicit expirations, island commonly times out after **1 hour** and focus card after **12 hours**.
- Client update: keep the notification ID stable, re-post with updated fields, and finish with `cancel(id)`.
- MiPush update: keep stable `notifyId` and order association, increment `sequence` strictly, and conclude with `cancel:true`.
- `timeout` is *not* equivalent to `islandTimeout`. Do not set `-1` as an attempt to create an eternal island; Xiaomi FAQ describes special short-lived behavior for `-1`.

Sources:
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2146
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144

## 3. Android publication and resource extras

### Official local flow

```kotlin
val notification = Notification.Builder(context, channelId)
    .setSmallIcon(R.drawable.ic_notification)
    .setContentTitle("Delivery in progress") // Normal Android fallback
    .setContentText("Driver is approaching")
    .setOnlyAlertOnce(true)
    .build()

notification.extras.putString("miui.focus.param", payloadJsonString)
notificationManager.notify(stableNotificationId, notification)
```

Use `NotificationChannel` for API 26+, runtime `POST_NOTIFICATIONS` for API 33+, and a `PendingIntent` leading to a relevant destination. On supported and **authorized** devices, SystemUI may consume OEM extras and render island state; otherwise the ordinary notification is still useful.

### Local picture resources

The string inside JSON such as `"pic": "miui.focus.pic_box"` must point to a real local resource in a **nested Bundle**:

```kotlin
val pics = Bundle().apply {
    putParcelable("miui.focus.pic_box", Icon.createWithResource(context, R.drawable.ic_box))
}
val extras = Bundle().apply {
    putBundle("miui.focus.pics", pics)
    putString("miui.focus.param", payloadJsonString)
}
val notification = Notification.Builder(context, channelId)
    .setSmallIcon(R.drawable.ic_notification)
    .setContentTitle("Fallback title")
    .setContentText("Fallback body")
    .addExtras(extras)
    .build()
```

Use local icons for local notification payloads. Avoid Base64 or raw binary inside the 3KB JSON string.

### Local action resources

Define a secure `PendingIntent`, wrap it in `Notification.Action`, store under `miui.focus.actions`, then reference the exact key in the **chosen supported template**:

```kotlin
val intent = Intent(context, DeliveryActionReceiver::class.java)
    .setAction("com.example.delivery.TRACK")
    .addFlags(Intent.FLAG_RECEIVER_FOREGROUND)
val actionIntent = PendingIntent.getBroadcast(
    context, 10, intent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
)
val action = Notification.Action.Builder(
    Icon.createWithResource(context, R.drawable.ic_track), "Track", actionIntent
).build()
val actions = Bundle().apply { putParcelable("miui.focus.action_track", action) }
// Merge with the picture Bundle and put under "miui.focus.actions".
```

Implement receivers explicitly and avoid exporting them needlessly. The exact JSON location of an action reference depends on the selected expanded Focus Notification template; do not insert arbitrary action arrays into unsupported templates. Xiaomi documents an `actions` array pointing to `"action": "miui.focus.action_1"` for supported patterns.

A full Kotlin sample with a real JSON serializer is in [../examples/HyperIslandPublisher.kt](../examples/HyperIslandPublisher.kt).

## 4. MiPush publication and remote images

Xiaomi's Java server SDK uses a `Sender`, `Message.Builder`, stable `notifyId`, and `.extra("miui.focus.param", serializedJson)`; the documented direct send looks like `sender.send(message, regId, 3)`. The `3` here is a MiPush SDK send argument, **not** a HyperOS version check. See [../examples/MiPushServerExample.java](../examples/MiPushServerExample.java).

- **Authorization**: enable Xiaomi Push service and HyperIsland service, obtain approved scenarios, and follow the production verification process.
- **Targets**: Xiaomi's published guide currently specifies **`regId`** sending for this pathway.
- **Remote pictures**: pass `.extra("miui.focus.pic_<id>", "https://...")`. Images must use HTTPS, individual files should be <=100 KB, download timeout <=180 seconds, aspect ratio between 1:1 and 16:9, and no more than 10 per notification. Prefer fewer images.
- **Secrets**: keep MiPush application secrets on the server; never embed in app binaries or checked-in source.

Sources: https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131 and https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2146

## 5. Capability and focus-permission checks

**Protocol** (official non-reflection query):

```kotlin
val focusProtocol = Settings.System.getInt(
    context.contentResolver, "notification_focus_protocol", 0
)
val supportsHyperIsland = focusProtocol == 3
```

**Focus permission** (OEM provider; may block, throw or return `null`; query off main thread):

```kotlin
fun hasFocusPermission(context: Context): Boolean = try {
    val extras = Bundle().apply { putString("package", context.packageName) }
    context.contentResolver.call(
        Uri.parse("content://miui.statusbar.notification.public"),
        "canShowFocus", null, extras
    )?.getBoolean("canShowFocus", false) ?: false
} catch (_: Exception) {
    false
}
```

**Feature flag** (Xiaomi also documents reflection against `android.os.SystemProperties.getBoolean("persist.sys.feature.island", false)`). Because this is a hidden API, prefer the public Settings protocol check as a conservative gate; do not present successful reflection as proof of publication permission.

Always offer a plain Android-notification fallback if: `focusProtocol != 3`, authorization absent, Focus permission disabled, or renderer ignores extras. The fallback is an implementation recommendation, not a promise of system downgrade behavior in every custom ROM.

## 6. Templates and documented sample pitfalls

- Expanded Focus Notification templates and compact Summary Island templates are **enumerated and preapproved**, not arbitrary widget trees.
- `bigIslandArea` can include `imageTextInfoLeft`, `textInfo`, `picInfo`, etc.; exact component combinations are restricted by the official template list.
- Use the reviewed [2026-01-29 component extraction](hyperos3-component-schema.md) together with the official library and developer guide for field-level compatibility, especially `baseInfo`, `hintInfo`, timers, animated pictures or action layouts. An extracted JSON table is not device certification.
- **Known copy-paste issues**: The public guide's integrated sample contains an unusual field name `"miui.focus.paramtextInfo"` and pseudo-Java JSON quoting that is not directly compilable. Treat this as a probable documentation transcription issue, **not a schema recommendation**. Canonical examples and community toolkit models use `textInfo` within `imageTextInfoLeft`. Always validate exact keys against Xiaomi's latest library and test on an approved device.
- Do not confuse `bigIslandArea` (compact summary to either side of the camera) with the expanded focus card rendered from separate template data.
- Local picture/action Bundles are not directly serialized into `miui.focus.param`. Preserve reference names exactly.

Official templates and docs (HyperOS 3 usage only):
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143
