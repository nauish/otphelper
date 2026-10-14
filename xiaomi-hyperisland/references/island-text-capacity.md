# Official Xiaomi PDF: Island Character Capacity Guidelines

**Authority:** OFFICIAL XIAOMI. **Document:** `Island Character Capacity Guidelines` (Chinese: official `dao zifu shuliang guifan shuoming` PDF), linked at the end of the [official Summary-State Design Standard](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143). **Verified 2026-10-14 by reading the actual 3-page PDF and inspecting screenshots of all 3 pages.**

[Open the original 3-page PDF](https://mag-admin.cnbj1.mi-fds.com/mag-admin/island/%E5%B2%9B%E5%AD%97%E7%AC%A6%E6%95%B0%E9%87%8F%E8%A7%84%E8%8C%83%E8%AF%B4%E6%98%8E.pdf)

This is an English translation and practical implementation guide. It is *not* the same document as the approximately 34 MB official `20260129` template-library PDF.

## Page 1: Overflow hierarchy and text regions

**Universal compression priority (applies when space runs out):**

1. Reduce the primary large-text size to the small-text size.
2. If content still does not fit, hide the optional small text.
3. If it still does not fit, apply end-of-container fade-to-black/clipping. **No scrolling is promised.**

For text-summary templates, the **large primary text is required** and the **small auxiliary text is optional**. Under the state where the large font **has shrunk** to the small font size, the official examples guarantee (across models, for Chinese copy):

| Region | Combined capacity | Supported large/small split examples |
|---|---|---|
| A (left of camera) | Up to 4 Chinese characters | 4+0, 3+1, 2+2, 1+3 |
| B (right of camera) | Up to 4 Chinese characters | 4+0, 3+1, 2+2, 1+3 |

A documented illustrative fit is `XX:XX delivered` where `XX:XX` uses roughly the width of 2 Chinese characters and the whole expression uses roughly 4 units (original document's Chinese example). **Do not equate 4 Chinese characters to four English characters** or to arbitrary emoji; glyph widths differ.

## Page 2: Preserving big-type size and fixed-width digits

If the large text should **stay large without auto-shrinking** on all tested-model reference configurations:

| Region | Example large/small split |
|---|---|
| A (left) | 2 large + 1 small, or 1 large + 2 small |
| B (right) | 2 large + 1 small, or 1 large + 2 small |

The original PDF explicitly cautions that a device with the smallest available area is used for the comparison illustrations; the actual cap depends on **device, number of simultaneous islands, and sizing behavior**.

For **fixed-width digit components**:

- Numbers are required; adjacent small-unit text is optional and may disappear when width is insufficient.
- **A region:** up to **3 digits**, plus **1 Chinese character** or **2 Latin letters** in the small-unit slot.
- **B region:** up to **3 digits**, plus **2 Chinese characters** or **2 Latin letters** in the small-unit slot.
- Design units such as `km` or `mm` to fit the dedicated optional unit area; do not concatenate arbitrary four- or five-digit values.

## Page 3: Visual examples

The PDF depicts a dark capsule around the camera, with a square icon and compact number + `km` on the left and another compact number + `mm` on the right. Alternative illustrations show Chinese-unit text instead. Use these screenshots **as layout references, not as precise measurements or a custom canvas implementation**.

## Applying the PDF to English UI copy

**OFFICIAL RULE:** Treat the Chinese-character budgets above as *Chinese text guidance*, not guaranteed pixel widths on every phone. **IMPLEMENTATION RECOMMENDATION:**

1. Put the smallest stable icon first; choose the single most meaningful number/status.
2. Avoid multiword status phrases in A/B. For example, prefer `5` + `min` to `Driver arriving in five minutes` in the compact island; put complete text in the expanded card and Android fallback.
3. Simulate narrow phones, a second simultaneous island, different font scales, and both light/dark modes.
4. Check whether the main text shrinks, optional text vanishes, or the end fades. Critical information must remain discernible in every tested state.
5. Pair color highlights with text/icon shape; do not depend solely on color. Try alternate-language lengths.
6. For numeric values exceeding 3 digits, show a rounded unit or a different template (if approved); do not force long numbers into the fixed-width region.

## Evidence table

| Guideline | Original PDF page (1-based) | Verification |
|---|---|---|
| Shrink -> hide optional -> clip, 4-character Chinese combined budget | 1 | PDF text + visual screenshot |
| Keep-large 2+1 / 1+2, and fixed-width digit budgets | 2 | PDF text + visual screenshot |
| Capsule and sample numeric-unit layouts | 3 | Visual screenshot |

These page references are **only** for the 3-page character-capacity PDF. The large template-library PDF was not opened page-by-page in this environment; do not invent page references to it.
