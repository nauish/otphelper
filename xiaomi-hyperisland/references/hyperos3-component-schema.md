# HyperOS 3 HyperIsland component contract (2026-01-29 template extraction)

**Scope:** HyperOS 3 only. **Input evidence:** user-supplied `小米超级岛模板库20260129.md` (a text/Markdown conversion of Xiaomi's official dated template library), compared against Xiaomi's [expanded](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142), [summary](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143), and [developer API](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131) pages on 2026-10-14.

**Extraction quality:** The converted file includes replacement characters (`�`), image OCR text, shifted template headings, misspellings (`booean`, `foucs`), and inconsistent `timerCurrent` vs `timerSystemCurrent` examples. Field tables below are normalized *only* where the table clearly supports the name or type. Flag discrepancies explicitly; never copy malformed JSON blocks verbatim. The original official PDF/Figma drawings and authorized device rendering remain authoritative for production.

## 1. Component map

| Expanded component type | JSON property | Core fields (where present) |
|---|---|---|
| Text component 1/2 | `baseInfo` | `type`, `title`, `content`, `subTitle`, `subContent`, `extraTitle`, `specialTitle`, colors, divider flags |
| IM Image/Text | `chatInfo` | `picProfile`, `title`, `content`, `appIconPkg`, timer, light/dark colors |
| Emphasized Image/Text | `highlightInfo` | `title` or `timerInfo`, `picFunction`, `content`, `subContent` |
| Recognition Graphic 1/2/3 | `picInfo` | `type`, `pic`, `picDark`, optional `actionInfo` |
| Pictorial countdown | `picInfo` | `type: 5`, `pic`, `picDark`, `title`, `colorTitle` |
| Progress 1 (moving art) | `progressInfo` | `progress`, colors, `picForward`, `picMiddle`, `picMiddleUnselected`, `picEnd`, `picEndUnselected` |
| Progress 2 (simple bar) | `progressInfo` | `progress`, `colorProgress`, `colorProgressEnd` |
| Progress 3 (segmented) | `multiProgressInfo` | `title`, `progress`, `color`, `points` |
| Button 1 (action group) | `actions` | list of `actionInfo` with `type`, optional `progressInfo`, and action route |
| Button 2/3 | `hintInfo` | `type: 2` / `type: 1`, text/timer fields, `actionInfo` |
| Button 4 | `textButton` | array of one or two action objects |
| Button 5 | `highlightInfoV3` | `primaryText`, `secondaryText`, highlight tag/colors, `actionInfo` |
| Cover | `coverInfo` | `picCover`, `title`, `content`, `subContent` |
| New Icon/Text | `iconTextInfo` | `animIconInfo`, `title`, `content`, optional `subContent` |
| Template background | `bgInfo` | `type`, `picBg`, `colorBg` |

**Context:** These names are component payload members inside the chosen `param_v2` template. Their presence **does not authorize mixing them** in unsupported compositions. [Template matrix](official-template-catalog.md) defines the legal combinations.

## 2. Expanded text and image fields

### `baseInfo` — text component, types 1 and 2

| Field | Data type | Required / meaning |
|---|---|---|
| `type` | integer | **Required**; `1` for Text 1 or `2` for Text 2 |
| `title` | string | **Required** primary text 1 |
| `content` | string | **Required** secondary text 1 |
| `subTitle` | string | Optional primary text 2 |
| `extraTitle` | string | Optional supplementary primary text |
| `specialTitle` | string | Optional highlighted tag |
| `subContent` | string | Optional secondary text 2 |
| `picFunction` | string | Optional functional icon resource key |
| `showDivider` | boolean | Show a divider between text fragments |
| `showContentDivider` | boolean | Divider between secondary copy and functional icon; exact placement differs by text type |
| `colorTitle`, `colorTitleDark`, `colorSubTitle`, `colorSubTitleDark`, `colorExtraTitle`, `colorExtraTitleDark` | strings | Optional theme-aware text colors |
| `colorSpecialTitle`, `colorSpecialTitleDark`, `colorSpecialBg` | strings | Tag text/background colors; verify dark background variant support in final system template |
| `colorContent`, `colorContentDark`, `colorSubContent`, `colorSubContentDark` | strings | Secondary-copy colors |

Example extracted and normalized:

```json
"baseInfo": {
  "type": 2,
  "title": "Driver arriving",
  "content": "Pickup in about 5 min",
  "subTitle": "AB-1234",
  "showDivider": true,
  "colorTitle": "#000000",
  "colorTitleDark": "#FFFFFF"
}
```

**Overflow order from official library:** for the main row, truncate supplemental text before primary titles and special tag; for secondary row, truncate `content`/`subContent` before the functional icon. The platform renders ellipses; keep critical information in the early visible portion.

### `chatInfo` — IM or call/transfer image + text

`picProfile` (required picture key; design >=224x224 px), optional `picProfileDark` and `appIconPkg`, required `title` and `content`, optional colors (`colorTitle`, `colorTitleDark`, `colorContent`, `colorContentDark`) and `timerInfo`. For the application icon, Xiaomi normally falls back to the launcher icon, custom suggested >=96x96 px. Image keys must resolve in picture extras.

### `highlightInfo` — emphasized copy or timer

`title` **or** a timer object; `picFunction` required, `picFunctionDark` optional; secondary `content` and `subContent` optional. `type: 1` is described as hiding auxiliary text 1, not as an interchangeable expanded-template ID. Support `colorTitle[Dark]`, `colorContent[Dark]`, and `colorSubContent[Dark]` where the chosen layout permits.

### `picInfo` — recognition icon and picture countdown

**Recognition types:** `1` = app icon, `2` = middle graphic, `3` = large graphic. The source table labels `pic` and `picDark` as required, but type 1 also describes using the system launcher icon; verify whether the field may be omitted for your selected icon path on device. For types 2 and 3 supply an image reference key that resolves in `miui.focus.pics` (or cloud transport).

**Pictorial countdown:** `type: 5`, `pic`, `picDark`, `title`, `colorTitle` required per table; color is an ARGB color string such as `#CC234567`, not necessarily RGB. The image should have matching light/dark variants, >=96x96 px. Example:

```json
"picInfo": {
  "type": 5,
  "pic": "miui.focus.pic_light_red",
  "picDark": "miui.focus.pic_light_red_dark",
  "title": "12",
  "colorTitle": "#CC234567"
}
```

### `iconTextInfo` and `animIconInfo` — newer image/text

`iconTextInfo`: required `animIconInfo` object, `title`, `content`; optional `subContent` plus title/content colors and dark variants. The visual element is **48x48 dp** inside a **56x56 dp** visible area; image recommended >=224x224 px.

`animIconInfo` table describes `type: 0` as default static art and `src` as a picture-bundle key; optional `srcDark`. **Source conflict:** the converted example shows `type: 3` although the table only defines `0`. **Do not assume `3` is valid** without inspecting the official file/device. For a static asset start with documented `type: 0`.

### `coverInfo` — portrait cover / ticket artwork

Required: `picCover`, `title`, `content`, `subContent`. Light/dark color variants for all text fields. Suggested image at least **224x288 px**; if rounded, radius ~25% of displayed short side. The image is vertically aligned with the text group.

### `bgInfo` — optional background

`type: 1` = full background (default), `type: 2` = right area; optionally `picBg` and `colorBg`. Use only if allowed for your selected official expanded template; don't override the system pill background or pretend fully customizable overlays.

## 3. Timer contract

The converted library documents a reusable `timerInfo` in `chatInfo`, `highlightInfo`, `hintInfo`, and `sameWidthDigitInfo`:

| Key | Type | Meaning |
|---|---|---|
| `timerType` | integer, **required when timer supplied** | `-2` countdown paused; `-1` countdown running; `0` nonrunning/default (a same-slot text headline is required); `1` stopwatch running; `2` stopwatch paused |
| `timerWhen` | long | Timestamp in **milliseconds** |
| `timerTotal` | long | Timer duration/progress according to chosen timer type |
| `timerSystemCurrent` | long | Device/reference time for drift adjustment, milliseconds |

**Known error:** some JSON samples in the Markdown use `timerCurrent`, while the table uses `timerSystemCurrent`. Prefer the *field table* as a candidate but check exact spelling in the official SDK/template document and a real authorized device. Do not invent timer types or claim that setting `timerType: 0` starts a timer.

## 4. Progress contract

### `progressInfo`: Progress 1 — custom artwork

- Required `progress` (integer), `picForward`, `picMiddle`, `picMiddleUnselected`, `picEnd`, `picEndUnselected`; optional `colorProgress`, `colorProgressEnd`.
- Use actual completed fraction mapped to Xiaomi's progress value; sample uses `40` for 40%.
- Forward asset canvas 60x47 dp exported >=240x188 px, <100 KB; suggested drawable subject area 44x39 dp. Intermediate/target canvas 30x47 dp exported >=120x188 px, <100 KB.
- Before crossing a node, the guidance suggests a grey larger marker adjacent to the bar; after crossing, use a smaller accent-colored raised marker plus node dot.

```json
"progressInfo": {
  "progress": 40,
  "colorProgress": "#FF8514",
  "colorProgressEnd": "#FF8514",
  "picForward": "miui.focus.pic_forward_v2",
  "picMiddle": "miui.focus.pic_middle_v2",
  "picMiddleUnselected": "miui.focus.pic_middle_off_v2",
  "picEnd": "miui.focus.pic_end_v2",
  "picEndUnselected": "miui.focus.pic_end_off_v2"
}
```

### `progressInfo`: Progress 2 — simple bar

Contains `progress` (required), optional `colorProgress` and `colorProgressEnd`; **no image keys**. Same start/end gives flat color; different start/end gives gradient; Xiaomi recommends same-color-family gradients.

### `multiProgressInfo`: Progress 3 — segmented progress

`title` (required description), `progress` (required integer), optional `color` and `points` (0–4 nodes). The source describes up to **4 segments**, max overall width **336 dp** and compressed label width **72 dp** (6 Chinese / 12 Latin characters). The number of segments and nodes varies by chosen template; the source's wording of 0–4 nodes deserves a UI check before generating a segmented progress geometry.

```json
"multiProgressInfo": {
  "title": "Processing",
  "progress": 40,
  "color": "#00FF00",
  "points": 2
}
```

## 5. Interactive buttons / pending intents

### Action reference methods

**Method A (recommended local route):** store a `Notification.Action` under `miui.focus.actions` bundle with key `miui.focus.action_<id>`; place that exact key in JSON `action`. **Method B:** build custom `actionInfo` containing `actionIcon`, optional `actionIconDark`, `actionTitle`, colors, and `actionIntent` with `actionIntentType`.

`actionIntentType`: `1` = Activity, `2` = BroadcastReceiver, `3` = Service; serialized Intent string from `Intent.toUri(Intent.URI_INTENT_SCHEME)`. Optional `clickWithCollapse` controls whether the expanded panel closes after click; Activity actions usually close automatically.

**Security caution, explicitly separate from vendor instructions:** The converted template library states that a custom intent targeting a `BroadcastReceiver` or `Service` may require `android:exported="true"` to dispatch on some devices. Exporting a component creates an external entry point. Restrict exported endpoints with a suitable signature permission, validate sender/data/authorization, and never expose privileged actions via an unprotected receiver. Prefer an explicit `PendingIntent` with `FLAG_IMMUTABLE` and an internal component where system behavior permits; test the exact OEM route.

### Button 1 `actions`

Array of `actionInfo` objects. `type`: `0` round/default, `1` progress button, `2` text button. **1–3** round or progress actions, **one** text action only, no mixing with text action. `type: 1` requires nested `progressInfo` (documented `progress`, optional `colorProgress`, `isCCW`, `isAutoProgress`). `isCCW: false` starts at 3 o'clock (0 degrees); `true` starts at 12 o'clock (270 degrees). `isAutoProgress` is described as automatic progress updates; do not guess auto-refresh timing.

### Button 2 or 3 `hintInfo`

The source maps **Button 2 -> `hintInfo.type: 2`** and **Button 3 -> `hintInfo.type: 1`**. Includes `title` or `timerInfo`, optional `subTitle`, required `content`, optional `subContent`, theme-aware title/content colors, and required `actionInfo`. For type 1, UI description also includes a special tag label, optional icon `picContent`, and `colorContentBg`. These variants have different visible arrangements; don't treat them as the same template merely because they share a JSON parent name.

### Button 4 `textButton`

One or two `actionInfo` objects in an array. Supports `actionTitle`, colors including light/dark text and normal/pressed backgrounds, and the same action reference/custom-intent routing model.

### Button 5 `highlightInfoV3`

`primaryText` required (minimum compressed width cited **132 dp** / 6 Chinese / 12 Latin units), optional `secondaryText` (**84 dp**), `showSecondaryLine`, and tag `highLightText` (maximum **72 dp** / 6 Chinese / 12 Latin units); color pairs `primaryColor[Dark]`, `secondaryColor[Dark]`, `highLightTextColor[Dark]`, `highLightbgColor[Dark]` with required `actionInfo`. Keep field capitalization exactly as documented until the official JSON renderer proves otherwise (`highLight*` intentionally mixed-case).

## 6. Summary big-island component fields

| Summary area and type | Field schema / notes |
|---|---|
| A `imageTextInfoLeft` type **1** | Optional `picInfo` and `textInfo`; at least icon or major text content. `picInfo`: `{type:1, pic: ...}`. `textInfo`: `title`, optional `content`, `narrowFont`, `showHighlightColor`. Example conversion omits `frontTitle` on A-type 1 but other docs include it; validate on device. |
| A `imageTextInfoLeft` type **5** | Required icon and text; `picInfo.type:4` for static graphic in converted table, `textInfo.title` required, optional `content`, `showHighlightColor`. Numeric area up to three digits or two Chinese characters. |
| B `textInfo` | `title` required; optional `frontTitle`, `content`, `narrowFont`, `showHighlightColor`. Use at most two text fragments where possible. |
| B `imageTextInfoRight` type **2** | `picInfo` plus `textInfo` with required `title`, optional `frontTitle`, `content`, `narrowFont`, `showHighlightColor`. |
| B `imageTextInfoRight` type **3** | `picInfo` plus `textInfo.title` required; field table lists `narrowFont` and `showHighlightColor` options. |
| B `imageTextInfoRight` type **6** | `picInfo.type:4`, `pic`, and `textInfo.title` required; up to 3 digits. Also used in small-island style 3. |
| B `fixedWidthDigitInfo` | `digit` required; optional `content`, `showHighlightColor`. Fixed numeric slot displays 1–3 digits; test decimals carefully (source sample is `99.9` despite 3-digit guidance). |
| B `sameWidthDigitInfo` | `digit` or `timerInfo`; optional `content`, `showHighlightColor`; use when digits change every second. |
| B `progressTextInfo` | `progressInfo.progress` required; optional `colorReach`, `colorUnReach`, `isCCW`; optional text object `frontTitle`, `title`, `content`, `narrowFont`, `showHighlightColor`. |
| B wide `picInfo` | `type:1` and `pic` for a static picture; follow official wide-image layout ratios. |

### Summary image resolution and text behavior

- Small/large island square icons: recommended >=88x88 px.
- Wide B icon in types 2/3: <=~1.45:1 aspect ratio, >=128x88 px; B large picture <=~2.2:1, >=192x88 px.
- Big island text: ~4 Chinese characters per A/B group is the *recommended* compact design budget, not a universal English string-length API limit. Longer text shrinks, hides optional segments, then clips; it does **not** marquee.
- Fixed-width numeric B region supports 1–3 digits. The separate official character PDF documents how short unit strings fit, as described in [island-text-capacity.md](island-text-capacity.md).

## 7. Summary small-island component fields

- Icon style: `smallIslandArea.picInfo = {"type":1,"pic":"miui.focus.pic_<id>"}`.
- Icon + ring: `smallIslandArea.combinePicInfo = {"picInfo":{"type":1,"pic":"..."},"progressInfo":{"progress":40,"colorReach":"#...","colorUnReach":"#..."}}`; optional `smallPicInfo` is mentioned in the source table and needs template-specific testing.
- Icon + number: `smallIslandArea.imageTextInfoRight` with `type: 6`, `picInfo.type:4`, and `textInfo.title` containing up to three digits.
- **Possible source typo:** a converted cell prints `miui.land.pic_xxx`, while the developer API and other rows use `miui.focus.pic_*`. Do **not** synthesize a different Bundle namespace from that isolated line; reconcile against the official developer documentation and the actual device.

## 8. JSON example: progress summary with approved template shape

The following is a **syntactic component example**, not permission/approval evidence and not a full device-certified `param_v2` envelope:

```json
{
  "bigIslandArea": {
    "imageTextInfoLeft": {
      "type": 1,
      "picInfo": {"type": 1, "pic": "miui.focus.pic_file"},
      "textInfo": {"title": "File", "showHighlightColor": false}
    },
    "progressTextInfo": {
      "textInfo": {"title": "40%"},
      "progressInfo": {"progress": 40, "colorReach": "#FF8514", "colorUnReach": "#666666"}
    }
  },
  "smallIslandArea": {
    "combinePicInfo": {
      "picInfo": {"type": 1, "pic": "miui.focus.pic_file"},
      "progressInfo": {"progress": 40, "colorReach": "#FF8514", "colorUnReach": "#666666"}
    }
  }
}
```

This corresponds to summary template **5** and small template **2**. The picture key must resolve to a proper local `Icon` in the `miui.focus.pics` `Bundle` or a valid HTTPS cloud extra. For full envelope/update/cancel instructions see [official-api.md](official-api.md).
