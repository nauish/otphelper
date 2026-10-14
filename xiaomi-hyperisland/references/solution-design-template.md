# HyperOS 3 HyperIsland scene-design and approval handoff

**Authority:** OFFICIAL XIAOMI [Solution Submission Guide](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144); this English worksheet is an **implementation adaptation**. The official page provides a submission `.docx` and an editable [Figma `.fig` design reference](figma-design-reference.md). These are not substitutes for production authorization.

## 1. Required UX proposal per approved business scene

1. Scenario: real service, value to the user, actual `business` scene code (or "approval pending"), owner and transport.
2. All lifecycle nodes, exact triggers and timings, whether first publication or update should auto-expand, cancel/error behavior.
3. For each node: **big island A/B**, **small island**, **expanded card**, Focus Notification in the shade, lock-screen/AOD where used, and regular Android notification.
4. Template IDs: one big island 1–9, small island 1–3, expanded official ID from [the matrix](official-template-catalog.md). Match every chosen component's required JSON fields.
5. Assets: dimensions and sharpness, light/dark icon and color variants, exported Figma frames, actionable secure `PendingIntent` mapping.
6. Timeouts: notification in **minutes**, island in **seconds**; default expansion approximately **5 seconds** when triggered. End task deliberately.
7. QA coverage: font scale, theme, multiple islands, privacy/lock screen, permissions, upload/download retries, foldable outer displays, and device screenshots/video.

## 2. Reusable proposal worksheet

```markdown
# HyperOS 3 HyperIsland Scenario: <scene>
Approval: pending | approved [record ID]
Transport: Android Notification | authorized MiPush
Business code: <real Xiaomi-approved value>
Design source: official Xiaomi .fig + current official template page

Chosen templates:
  Big: #<1..9> [approved A/B pairing]
  Small: #<1..3>
  Expanded: #<official expanded ID>

| Stage | Trigger | Big A | Big B | Small | Expanded + actions | Auto-open | Expiry / cancel |
|---|---|---|---|---|---|---|---|
| Create | ... | ... | ... | ... | ... | ... | ... |
| Update | ... | ... | ... | ... | ... | ... | ... |
| Complete | ... | ... | ... | ... | ... | ... | ... |
| Failure | ... | ... | ... | ... | ... | ... | ... |

AOD / lock screen: <safe short information>
Regular Android notification: <title, body, safe intent>
Icons: <light/dark src, px, export scale, picture resource key>
Action security: <local PendingIntent or protected exported component>
State privacy, accessibility, performance and real-device evidence: <...>
```

## 3. Worked scene: pickup ETA

Select expanded **4** (Text 2 + Recognition 1 + Progress 1), big **7** (Image/Text 1 + fixed-width digits), small **1** (icon).

```text
BIG:       [car + "Ride"] [camera] [5 min]
SMALL:     [car icon]
EXPANDED:  "Driver arriving" + ETA + accurate route progress + approved actions
AOD:       "Pickup in about 5 min" (suppress personal data as appropriate)
NORMAL:    "Ride confirmed — driver ~5 minutes away" / open-ride intent
```

| Stage | Auto expand? | Update | Close |
|---|---|---|---|
| Driver accepts | Possibly once | Driver status and ETA | No |
| ETA changes | Normally no | Numeric value, stable notification ID | No |
| Driver arrives | Only if justified | Arrival and short action | After pickup |
| Ride ended/cancelled | No | Optional final ordinary notification | Cancel island ID |

## 4. Worked scene: file transfer

Select expanded **21** (IM Image/Text + Progress 2), big **5** (Image/Text 1 + Progress/Text), small **2** (icon + ring). Actual progress must be reported, not decorative. On completion, failure or explicit cancel, close the island and preserve a clear normal notification if needed.

## 5. Review gates

- [ ] Use one of Xiaomi's enumerated template combinations, not an arbitrary Figma composition.
- [ ] Scene and business code approved, or clearly pending.
- [ ] All start/update/finish/error states mocked up in big/small/expanded modes.
- [ ] Official `.fig` imported and compared with current online rules; attach relevant frame/screenshots.
- [ ] Asset size, dark/light colors, text widths and truncated-copy states inspected.
- [ ] Consent/privacy rules tested for lock screen and AOD; no accidental OTP/address leakage.
- [ ] Local/cloud picture references resolve; button intents are secured and functional.
- [ ] Stable IDs, cloud sequence, duration, cancellation and fallback verified on real HyperOS 3 hardware.
- [ ] Approved release APK and scenario validation evidence are ready for Xiaomi review.

Sources: [Official Submission Guide](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144), [expanded](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142), [summary](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143), [onboarding](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2132).
