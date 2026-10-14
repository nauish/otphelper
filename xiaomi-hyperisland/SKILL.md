---
name: xiaomi-hyperisland
description: Design, implement, audit, and validate Xiaomi HyperOS 3 HyperIsland (Super Island) integrations. Use for official Xiaomi miui.focus.param / param_v2 JSON, Android Notification or MiPush publication, Kotlin and Java wrappers, compact big/small islands, expanded component templates, progress, timer and action UX, official 2026-01-29 template library, official Xiaomi Figma design reference, technical constraints and production approval. This skill targets HyperOS 3 exclusively.
---

# Xiaomi HyperIsland — HyperOS 3 Developer Skill

**Target:** Xiaomi HyperOS 3 only. **Research verified:** 2026-10-14. Write developer-facing artifacts, comments, code and documentation **in English** unless the requester explicitly chooses another language.

## Mandatory rules

1. **Only implement HyperOS 3.** Gate the island UI on the official system protocol query returning **3**. Do not implement or describe compatibility branches for earlier HyperOS releases. A *normal Android notification* is a valid diagnostic/permission fallback, not an older-island integration.
2. **Prefer Xiaomi's authorized API.** Publish an Android `Notification` with the OEM `miui.focus.param` JSON extra and optional `miui.focus.pics` / `miui.focus.actions` Bundles, or send authorized MiPush notifications. Neither JSON nor a third-party wrapper bypasses Xiaomi service/scene review.
3. **Use fixed official templates.** Choose exactly one published **big summary** template (1–9), one **small island** template (1–3), and one official **expanded** template (1–13, 14-1, 14-2, and 16–22). Do not freely combine unrelated components. Template numbering follows [the live official page](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142); a converted Markdown source has a documented shift in late template numbers.
4. **Preserve source confidence.** Tag each assertion `OFFICIAL XIAOMI`, `USER-SUPPLIED TEMPLATE EXTRACTION`, `COMMUNITY WRAPPER`, or `ILLUSTRATIVE`. Do not silently trust OCR-broken quotes or inconsistent field samples. Do not invent scene `business` entitlements, library releases or dynamic visuals.
5. **Design all surfaces.** Include big A/B island, small island, expanded state, optionally AOD/lockscreen, and lifecycle create -> update -> finish. Use accurate constraints from the official design reference and character-capacity PDF.
6. **Use sound Android security.** Provide a notification channel, `POST_NOTIFICATIONS` handling (when applicable), a stable notification ID, a valid small icon and content intent, immutable explicit `PendingIntent`s, theme assets, JSON UTF-8 validation and cleanup. Minimize sensitive information on public/locked displays.
7. **Do not claim approval or successful on-device rendering** based solely on syntactic tests, Figma mockups, JSON schemas or a community test app.

## Source and reference order

Load only the files needed for the task:

| Task | Read before implementation |
|---|---|
| **Official API and transport** | [official-api.md](references/official-api.md) |
| **Template ID / layout choice** | [official-template-catalog.md](references/official-template-catalog.md) |
| **Exact component JSON fields** | [hyperos3-component-schema.md](references/hyperos3-component-schema.md) |
| **Official Figma reference** | [figma-design-reference.md](references/figma-design-reference.md) |
| **Copy and compact text capacities** | [island-text-capacity.md](references/island-text-capacity.md) |
| **Visual examples / UX hierarchy** | [design-patterns.md](references/design-patterns.md) |
| **Design submission** | [solution-design-template.md](references/solution-design-template.md) |
| **Wrappers, dependency caveats** | [wrappers.md](references/wrappers.md) |
| **Permissions, release, QA** | [rollout-checklist.md](references/rollout-checklist.md) |
| **Authority and provenance** | [sources.md](references/sources.md) |

**Source precedence:** current official Xiaomi developer page -> official 2026-01-29 template library fields as extracted in the user-uploaded Markdown (caveats documented) -> Figma visuals once actually inspected -> community libraries -> illustrative examples. Where two sources conflict, identify the conflict and require verification; do not silently choose the convenient JSON spelling.

## Quick API reference

| Item | Requirement |
|---|---|
| Local transport | Android `Notification.Builder` + `extras.putString("miui.focus.param", json)`; `NotificationManager.notify(stableId, notification)` |
| Server transport | Approved MiPush `Sender` / `Message.Builder().extra("miui.focus.param", json)` to `regId`; protect secrets |
| JSON root | `{"param_v2":{"business":"approved_code","param_island":{"bigIslandArea":{},"smallIslandArea":{}}}}`; shown empty areas are an envelope **illustration**, not a renderable design |
| Local pictures | `miui.focus.pics` Bundle keyed `miui.focus.pic_<id>`, values `Icon` |
| Local actions | `miui.focus.actions` Bundle keyed `miui.focus.action_<id>`, values `Notification.Action` |
| Updates | Same Android notification ID; for cloud updates supply valid `orderId` / increasing `sequence` |
| Stop | Client `NotificationManager.cancel(id)`; cloud documented `param_v2.cancel = true` |
| Lifetimes | `param_v2.timeout` = minutes; `param_island.islandTimeout` = seconds; documented defaults 720 min / 3600 sec |
| JSON size | Xiaomi FAQ push budget: <= **3,072 UTF-8 bytes**; check serialized JSON bytes |
| Version gate | `Settings.System.getInt(resolver, "notification_focus_protocol", 0) == 3` |
| Service permission | Xiaomi `content://miui.statusbar.notification.public` provider, method `canShowFocus`; handle absent permission/query failure |

See [official-api.md](references/official-api.md) for exact semantics, event behavior and MiPush image rules.

## Workflow

### 1. Choose implementation track

- **Official client (default):** Kotlin/Java Android app, Android Notification with `miui.focus.param`. Read [examples/HyperIslandPublisher.kt](examples/HyperIslandPublisher.kt) and [examples/README.md](examples/README.md). Attach actual icon/action Bundles. Check protocol 3 and scene permission; use plain Android notifications when approval/permission is unavailable.
- **Official cloud:** authorized MiPush server. Read [examples/MiPushServerExample.java](examples/MiPushServerExample.java). Maintain order identity and monotonic update sequence; place secrets only on the backend.
- **Optional community wrapper:** review [wrappers.md](references/wrappers.md); pin exact version and audit source, license, hidden APIs, and generated JSON. Community components are **not** Xiaomi official SDKs and **do not** grant entitlement.

### 2. Plan approved HyperOS 3 templates

Select all three:

- **Big summary**: A to the left of camera, B to the right. Only choose one of the nine official pairings.
- **Small summary**: icon; icon+ring; or icon+numeric text. Match specific `smallIslandArea` keys.
- **Expanded state**: choose one official expanded template and satisfy its required `baseInfo`/`chatInfo`/`iconTextInfo` and optional progress/button/cover fields. No custom Android Compose overlay can replace a template.

Read the [template matrix](references/official-template-catalog.md) **and** [component schema](references/hyperos3-component-schema.md). Pay attention to template-ID source discrepancy, unverified `animIconInfo.type` variants and `timerCurrent`/`timerSystemCurrent` transcription discrepancies. Treat the user-supplied 2026-01-29 Markdown as useful field evidence, not a copy-paste-ready JSON corpus.

### 3. Design in Figma and specify states

The [official Xiaomi Figma resource](references/figma-design-reference.md) is linked from Xiaomi's [solution-submission page](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144) as **《小米超级岛摘要态、展开态设计模板》** (`小米超级岛设计参考.fig`). Import the official file locally; it is a visual reference, **not** an API generator. Do not claim a value was extracted from its layers unless the `.fig` was actually inspected.

Use the [design worksheet](references/solution-design-template.md) to show each state: trigger, big A/B copy, small icon/ring, expanded text/actions, automatic expansion, timeout, update and cancellation, normal notification content, privacy and theme variants. Keep compact text within measured widths; use [the official 3-page character-capacity translation](references/island-text-capacity.md).

### 4. Build a tested JSON payload and resources

1. Serialize JSON with `JSONObject`/your testable serializer; do not concatenate strings or paste OCR-damaged sample snippets.
2. Populate `param_v2.business` using the actual approved Xiaomi business scene code. Keep `protocol` (the example value **1**) conceptually separate from the system protocol value **3**.
3. Populate `param_v2.param_island.bigIslandArea` and `.smallIslandArea` according to your selected templates and the [exact component reference](references/hyperos3-component-schema.md).
4. Populate expanded component objects for the selected expanded template; check mandatory fields and optional light/dark styles.
5. Resolve every `miui.focus.pic_*` reference in local picture Bundle or HTTPS MiPush extras; resolve `miui.focus.action_*` similarly. Protect custom exported actions if platform routing requires them.
6. Supply ordinary notification fallback with the same current task text and a safe content `PendingIntent`.
7. Update the same ID without repetitive unsolicited auto-expansion; cancel when completed, failed, expired, or user-canceled.

### 5. Validate and obtain approval

```bash
python scripts/validate_payload.py examples/package-delivery.json \
  --big-template 2 --small-template 1 --expanded-template 10 \
  --picture miui.focus.pic_box --action miui.focus.action_track
python scripts/validate_design_spec.py examples/ride-eta-design.json
python -m unittest discover -s scripts -p 'test_*.py' -v
```

Script success proves **structural/design preflight only**. Test on a whitelisted/authorized actual HyperOS 3 device, including current protocol, approved business, Focus entitlement, image Bundles, the three island states, daylight/night themes, translations, large font, foldable variant, AOD/privacy, order updates and cancellation. Follow [rollout-checklist.md](references/rollout-checklist.md).

## Required answer format for future requests

1. **Assumptions**: HyperOS 3, official vs community route, approved/pending scene, transport and SDK.
2. **Selected official template IDs**: big, small, expanded, with source links.
3. **Visual behavior**: A/B, compact, expanded, state transitions and accessibility.
4. **Code**: valid serialized envelope, picture/action Bundles, create/update/end, graceful regular-notification fallback.
5. **Testing**: JSON size/key checks, approval evidence, official Figma/design handoff, on-device results honestly labeled.
6. **Source status**: verified official guidance, extracted-library fields, and unresolved transcription issues.

## Example requests

- "Design a HyperOS 3 ride-ETA island with template 4 expanded, template 7 big summary and a 3-state Kotlin publisher."
- "Build a parcel delivery HyperIsland and validate `baseInfo`, `picInfo`, `hintInfo`, Android actions and icon resource Bundles."
- "Create a 2026-01-29-style Figma review handoff for a segmented smart-home progress card."
- "Review `timerInfo`, `multiProgressInfo`, `combinePicInfo`, and the component types in my HyperOS 3 payload."
- "Implement a secure MiPush real-time update sequence with approved scenes and cloud images."

**Samples:** [package-delivery.json](examples/package-delivery.json) · [ride-eta-design.json](examples/ride-eta-design.json) · [Kotlin publisher](examples/HyperIslandPublisher.kt) · [MiPush example](examples/MiPushServerExample.java).
