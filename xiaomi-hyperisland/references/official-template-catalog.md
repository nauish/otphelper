# HyperOS 3: approved Xiaomi HyperIsland template catalog

**Scope: HyperOS 3 only.** Evidence: Xiaomi's official [Expanded-State Design Standard](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142), [Summary-State Design Standard](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143), and the user-supplied text conversion of **Xiaomi Super Island Template Library, 2026-01-29** (`小米超级岛模板库20260129.md`). Reviewed 2026-10-14. English labels are explanatory translations; the numbered templates and component combinations remain Xiaomi-defined.

**Critical design rule:** Choose an enumerated fixed component composition. The expanded notification and summary island are *not* arbitrary view hierarchies, and Figma does *not* grant permission to submit a custom composition. Xiaomi must approve the actual service scenario and rendered design. For field-by-field objects consult [hyperos3-component-schema.md](hyperos3-component-schema.md).

## 1. Expanded-state template matrix — valid choices for HyperOS 3

| Official ID | Fixed composition | Example approved-design category (not business authorization) |
|---|---|---|
| 1 | Text component 1 + Recognition Graphic 3 | Weather/navigation |
| 2 | Text component 2 + Recognition Graphic 1 | Payment status |
| 3 | IM Image/Text + Recognition Graphic 2 | Phone/video call |
| 4 | Text component 2 + Recognition Graphic 1 + Progress 1 | Ride-hailing/delivery |
| 5 | Text component 1 + Recognition Graphic 1 + Progress 2 | Restaurant queue |
| 6 | Text component 2 + Recognition Graphic 1 + Progress 2 | Parking/charging |
| 7 | IM Image/Text + Recognition Graphic 1 + Progress 2 | Upload/download |
| 8 | IM Image/Text + Recognition Graphic 1 + Button 3 | Coupon or voucher update |
| 9 | Text component 2 + Recognition Graphic 1 + Button 2 | Movie ticket |
| 10 | Text component 2 + Recognition Graphic 1 + Button 3 | Parcel logistics |
| 11 | Emphasis Image/Text + Recognition Graphic 1 + Button 2 | Fitness session |
| 12 | IM Image/Text + Button 1 | Voice/video call control |
| 13 | Emphasis Image/Text + Button 1 | Recording |
| 14-1 | New Icon/Text | Navigation |
| 14-2 | New Icon/Text + Pictorial Countdown | Traffic-signal countdown |
| 16 | New Icon/Text + Button 1 | Verification code |
| 17 | New Icon/Text + Recognition Graphic 1 + Button 5 | Payment pending |
| 18 | New Icon/Text + Recognition Graphic 1 + Button 4 | Transfer/share |
| 19 | Cover + Recognition Graphic 1 + Button 5 | Ticket details |
| 20 | Text component 2 + Recognition Graphic 1 + Progress 3 | Data allowance |
| 21 | IM Image/Text + Progress 2 | Game/app download |
| 22 | New Icon/Text + Recognition Graphic 1 + Progress 3 | Smart-home/task status |

**Important source discrepancy:** The converted 2026-01-29 Markdown labels its late rows `15` through `21`; Xiaomi's currently published official design page labels the matching sequence `16` through `22` and has no separately enumerated expanded template `15`. Use **the current official online ID** for design submission. Do not silently derive IDs or trust broken OCR table borders. This discrepancy affects numbering, not necessarily the corresponding component description.

**Buttons:** Button 1 (`actions`) may contain 1–3 round buttons **or** 1–3 progress buttons **or** one standalone text button. Never mix a text button with other buttons. Other buttons (`hintInfo`, `textButton`, `highlightInfoV3`) are distinct structures and must match the chosen expanded template. A button's name does not imply its quantity.

## 2. Big summary island: nine supported A/B combinations

The camera divides the big island into **A (left)** and **B (right)**. Select exactly one of these combinations:

| Big ID | Region A | Region B | Suitable information |
|---|---|---|---|
| 1 | Image/Text 1 | Empty | Icon-only or short task status |
| 2 | Image/Text 1 | Text | Short status + short text |
| 3 | Image/Text 1 | Image/Text 2 | Connected device |
| 4 | Image/Text 1 | Image/Text 3 | Check-in |
| 5 | Image/Text 1 | Progress/Text | Active progress |
| 6 | Image/Text 1 | Equal-width digits/timer | Duration/countdown |
| 7 | Image/Text 1 | Fixed-width digits | ETA / distance |
| 8 | Image/Text 1 | Wide image | Music/device status |
| 9 | Image/Text 5 | Image/Text 6 | Icon + 3-digit metric |

For an A-region `imageTextInfoLeft`, the most frequently used `type` values are **1** and **5**, depending on the selected big template. For a B-region `imageTextInfoRight`, the referenced `type` values include **2**, **3**, and **6**. Other B components use `textInfo`, `progressTextInfo`, `fixedWidthDigitInfo`, `sameWidthDigitInfo`, or a wide `picInfo`. Match the *exact* selected pairing, not two convenient arbitrary objects.

## 3. Small summary island: three approved structures

| Small ID | Component | Data keys / constraints |
|---|---|---|
| 1 | Icon | `smallIslandArea.picInfo`; square image >= 88x88 px |
| 2 | Icon + circular progress | `smallIslandArea.combinePicInfo` with `picInfo` and `progressInfo`; optional small icon |
| 3 | Icon + numeric text | `smallIslandArea.imageTextInfoRight` **type 6**; up to three digits and >= 88x88 px square icon |

**Image fallback order** from the converted Xiaomi document: business-supplied small-island icon -> big-island A icon -> application icon. Compact text is recommended to fit **around four Chinese characters** per A/B text group; do not interpret this as a universal four-character limit in English. Refer to [island-text-capacity.md](island-text-capacity.md).

## 4. Image and progress design constraints

| Asset / component | Minimum or recommended specification |
|---|---|
| Compact summary icon | Square, >=88x88 px |
| Expanded functional icon in text | Square, >=80x80 px |
| Recognition Graphic 1 | Square, >=96x96 px; optional corner radius around one quarter of displayed side |
| Recognition Graphic 2 | Square, >=176x176 px |
| Recognition Graphic 3, new Icon/Text art, IM portrait | Square, >=224x224 px |
| Cover | >=224x288 px; optional corner radius one quarter of short side |
| Icon/Text button | >=96x96 px |
| Wide right-side summary icon | Aspect ratio <=~1.45:1; >=128x88 px |
| Wide summary picture | Aspect ratio <=~2.2:1; >=192x88 px |
| Progress 1 forward graphic | 60x47 dp canvas, >=240x188 px export, <100 KB, subject inside 44x39 dp area |
| Progress 1 intermediate/target graphic | 30x47 dp canvas, >=120x188 px export, <100 KB |
| Progress 2 bar | Real completion and theme-aware foreground/gradient; no custom nodes |
| Progress 3 segmented bar | Description + progress, 0–4 nodes, evenly divided segments |

**Expanded text truncation:** Primary line truncation order is supplemental text, then major titles, then special tags; secondary line truncation order is secondary text fields, then functional icon. The PDF-derived character capacity guidelines are a *different compact-surface rule*; do not conflate their sequence. Provide light/dark colors and bitmaps where a component permits them.

## 5. Mapping examples (recommendations, not guaranteed approvals)

| Live task | Expanded ID | Big ID | Small ID | Reason |
|---|---|---|---|---|
| Driver pickup ETA | 4 | 7 | 1 | Route progress + numeric ETA |
| Parcel delivery | 10 | 2 | 1 | Status and a single supported button row |
| Downloading | 21 | 5 | 2 | File art + honest linear/circular progress |
| Voice call | 12 | 6 | 1 | Caller data + timer/actions |
| Recording | 13 | 6 | 1 | Duration + stop/pause action |
| Ticket booking | 19 | 2 | 1 | Poster/cover and seat details |
| Smart appliance task | 22 | 5 | 2 | Stage progress and specific task status |
| Traffic signal ETA | 14-2 | 9 | 3 | Animated graphic + numeric countdown |

## 6. Design handoff and live verification

1. Select expanded, big, and small template IDs before writing JSON.
2. Map each component to the precise keys described in [hyperos3-component-schema.md](hyperos3-component-schema.md).
3. Obtain artwork and sizing from the official [Figma design reference](figma-design-reference.md); preserve approved slot geometry and system-owned transitions.
4. Specify every event/update/cancel state and whether expanded view opens automatically.
5. Verify in Xiaomi's authorized HyperOS 3 test path. A structurally valid JSON is **not** proof of a functioning or approved island.

Official references: [Expanded-State Guidelines](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142), [Summary-State Guidelines](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143), [Development Guide](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131), [Solution Submission](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144).
