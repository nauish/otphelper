# Xiaomi HyperIsland design patterns and annotated examples

**Authority:** official structural rules from Xiaomi; mockups and scenarios below are **ILLUSTRATIVE DESIGN**, not guaranteed pixel-accurate screenshots. Reviewed 2026-10-14.

## Contents

1. Design boundaries and compact states
2. Pattern gallery (transport, package, download, countdown, media)
3. State-machine planning worksheet
4. Accessibility and UX review

## 1. Design boundaries

- The **big compact island** sits to the left (**A**) and right (**B**) of the camera cutout. Official Xiaomi documentation lists two A-component families, nine B-options, and nine approved combinations. Do not freely assemble a custom combination.
- The **small island** uses the business icon where supplied; otherwise the big island A icon; otherwise the application icon.
- The **expanded card** is rendered using an approved Focus Notification layout, not an arbitrary Jetpack Compose UI or canvas. Xiaomi specifies that the card expanded from a summary island uses a dark background; notification shade cards can adapt to light/dark.
- On first appearance, `islandFirstFloat` controls opening the expanded view; update-time `enableFloat` controls expansion upon refresh. Avoid aggressive repeated expansions. Xiaomi reports an approximately **5-second** default expanded-state period.
- Compact text must be very short. Xiaomi recommends <= **four Chinese characters** per principal A/B text area; for English, **measure actual width on-device** rather than assuming a four-letter hard limit. Do not scroll clipped island text.
- Icons for compact island: square and approximately **88 x 88 px or better**. Expanded layout images: common vendor examples request 80, 96, 176, or 224 px square depending on the component; follow the selected template rather than scaling arbitrary art.
- B-side fixed-width numbers commonly show <= **three digits**. The supported narrow-font number style is useful for ETA, countdown, or progress.
- Avoid marketing/promo, upselling, ads, loans, and interactions that are not tied to a genuinely ongoing task; Xiaomi reviews scene suitability.

Official design:
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143 (Summary State Guidelines)
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142 (Expanded State Guidelines)
- https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144 (UX submission requirements)

## 2. Pattern gallery

### A. Ride arriving (HyperOS 3 expanded template 4)

**Official template recommendation:** Expanded template 4: **Text 2 + Recognition Icon 1 + Progress 1** (ride-hailing / delivery). For compact mode, choose an approved **Icon/Text A + Fixed-Width Number B** summary template (e.g. ETA counter).

```text
BIG SUMMARY   [A: car icon + "Pickup"] [camera] [B: "5 min"]
SMALL         [car icon]
EXPANDED      +---------------------------------------+
              | Driver arriving       5 min          |
              | Blue sedan  /  AB-1234              |
              | [o=============>----------o]        |
              | [View ride]         [Call driver]     |
              +---------------------------------------+
AOD           "Driver arriving in 5 min"
FALLBACK      "Ride arriving | ETA 5 min" (normal notification)
```

**Lifecycle:** accepted -> driver en route -> arrived -> picked up (dismiss or replace appropriately). Use unique update keys for the same ride; do not expose full personal addresses in public lock-screen views without consent.

### B. Parcel / order delivery (HyperOS 3 expanded template 10)

**Official template recommendation:** Expanded template 10: **Text 2 + Recognition Icon 1 + Button 3** (parcel/logistics). Big summary A: package icon + "On way"; B: a short ETA or stage code; small: package icon. Buttons might include "Track" or "Details", when supported by the chosen template.

```text
BIG SUMMARY   [A: box + "Parcel"] [camera] [B: "Today"]
SMALL         [box icon]
EXPANDED      +---------------------------------------+
              | Out for delivery                      |
              | Tracking # ending 28                 |
              | Expected today, before 18:00         |
              |                         [Track]       |
              +---------------------------------------+
AOD           "Parcel is out for delivery"
FALLBACK      "Package out for delivery | Today"
```

**Lifecycle:** packed -> in transit -> out for delivery -> delivered -> dismissed. The JSON [package-delivery.json](../examples/package-delivery.json) is a **template-shaped starting example**. Confirm approved keys and business scene before rollout.

### C. Upload/download progress (OS3 expanded example)

**Official template recommendation:** Expanded OS3 template 21: **IM Image/Text + Progress 2**. For summary, the small island can be icon + circular progress, big summary A can pair icon/percent with a B-side compact number.

```text
BIG SUMMARY   [A: download + "72%"] [camera] [B: "2 min"]
SMALL         [download icon, 72% ring]
EXPANDED      +---------------------------------------+
              | Downloading report                    |
              | 72% [====================------]      |
              | 2 minutes remaining                   |
              +---------------------------------------+
FALLBACK      Android progress notification (indeterminate or 72%)
```

**Lifecycle:** start -> progress (throttle updates) -> finished/error -> dismiss; update without repeated sound/vibration. Do not keep an island forever after completion.

### D. Countdown / appointment

**Official template recommendation:** Use approved **fixed-width numbers** / timer components; do not invent an interactive clock layout. Prefer clear time units and short text.

```text
BIG SUMMARY   [A: calendar icon] [camera] [B: "12m"]
SMALL         [calendar icon]
EXPANDED      "Boarding in 12 min" / gate / seat / "View pass"
FALLBACK      "Boarding at 14:30 | Gate B7"
```

Display actual event time and update only when meaningfully necessary; avoid changing a static notification every second if the system-supported timer template can do it.

### E. Music/video playback

**Official note:** Xiaomi documents automatic island presentation for correctly integrated **media notifications**. Use Android media sessions/MediaStyle and Xiaomi's media adaptation guide rather than inventing a custom media business payload. Drag-share integration is a separate `miui.focus.param.media` pathway and should be implemented only when relevant.

```text
BIG SUMMARY   [A: album art / track] [camera] [B: waveform / controls]
SMALL         [album art]
EXPANDED      Playback controls + track title per media system presentation
FALLBACK      Android media player notification
```

Media guide: https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2162

## 3. State-transition worksheet

For any new business scenario, fill this table before writing code:

| Event | Big / small summary | Expanded details | Auto-expand? | Update identity | End behavior |
|---|---|---|---|---|---|
| Create | Icon + initial state | What begins, next useful step | Usually once, if important | Set stable ID and order ID | None |
| Significant change | New ETA/progress | What changed + safe action | Only for major changes | Same ID, MiPush next `sequence` | None |
| Minor refresh | Updated number | Same template | Usually **no** | Same ID; throttle updates | None |
| Completed / failed | Completion/error | Outcome and next step | Optional once | Same ID | Cancel promptly or short expiry |
| User dismisses / cancels | None | None | No | Mark canceled | `NotificationManager.cancel` / MiPush `cancel:true` |

For Xiaomi solution submission, explicitly show **all nodes**, trigger times, auto-expand nodes, compact and expanded mockups, Focus Notification/AOD views, and notification/island lifetimes.

## 4. UI review checklist

- Is the compact A/B content readable at a glance and a single value visually dominant?
- Does small island remain recognizable when the business-supplied icon is absent?
- Do expanded details provide a useful new fact or action, not duplicate text?
- Do colors have sufficient contrast in dark expanded cards and in light/dark notification shade?
- Is the action discoverable, accessible, and handled by a secure PendingIntent?
- Are sensitive personal details redacted on the lock screen where appropriate?
- Are English, Chinese, and larger accessibility text settings tested for overflow?
- Are icon sizes/square ratios, timer data, and version template differences respected?
- Is the normal Android notification fallback still usable when island permission is unavailable?
- Will the island disappear when the underlying live task finishes, not only at its 60-minute fail-safe?
