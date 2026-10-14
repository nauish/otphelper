# Official Xiaomi HyperIsland Figma design reference

**Authority:** OFFICIAL XIAOMI link, not a community recreation. **Platform scope:** HyperOS 3. **Last verified:** 2026-10-14.

## Official access

Open Xiaomi's [Solution Submission / UX Review page](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144) and select **《小米超级岛摘要态、展开态设计模板》** (Xiaomi Super Island Summary- and Expanded-State Design Templates). Xiaomi's download link resolves to **`小米超级岛设计参考.fig`** (a native Figma import file). The page also links **《开发者接入小米超级岛方案提报模板》** (a Word submission document).

The `.fig` download URL is hosted on Xiaomi's `mag-admin.cnbj1.mi-fds.com` domain. Prefer accessing the official page, then using its resource link; generated signed asset URLs may change. **This package includes the official locator and use instructions, not a copy of the proprietary `.fig` binary**: the downloader could confirm the website link but could not retrieve/import and visually inspect the binary in the current environment. Do not state that individual Figma measurements, layer names, color tokens, or motion curves were extracted from the file.

## Use in design projects

1. From the Xiaomi developer page, download `.fig` to a workstation with Figma access.
2. In Figma, use **File > Import** or drag the `.fig` file onto the file browser; create a working copy. Preserve the official master file for comparison.
3. Look for *summary big island A/B*, *summary small island*, *expanded Focus Notification* and any *cover/flip* reference frames. These labels describe expected surfaces, **not inspected layer names**.
4. Select the actual preapproved compositions from [official-template-catalog.md](official-template-catalog.md), rather than freely combining components from different frames.
5. Use Figma visuals to check artwork proportions, colors, theme variants, layout hierarchy and mockups. Use [hyperos3-component-schema.md](hyperos3-component-schema.md) for JSON and resource fields; a design frame is not an API contract.
6. Produce a scene handoff with every lifecycle state, big/small/expanded designs, timer/progress variations, privacy behavior, AOD, and normal-notification text. Attach native frame screenshots and the approved Xiaomi template numbers for the review.
7. Verify actual platform rendering with an authorized HyperOS 3 build and make corrections based on on-device behavior.

## What can be asserted without opening the Figma binary

- Xiaomi publicly links this `.fig` source in the **official** Solution Submission Guide.
- The official summary layouts have camera-adjacent A/B regions and approved small-island styles (cross-check [Summary Guidelines](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143)).
- The official expanded patterns are fixed component combinations (cross-check [Expanded Guidelines](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142)).
- Art recommendations come from the public official design pages and the user-supplied 2026-01-29 template Markdown, **not from uninspected Figma layers**.

## Checklist for an agent with connected Figma access

- [ ] Download/import the actual Xiaomi `.fig` reference.
- [ ] Record exact frame names, design dimensions, paddings, corner radii and type sizes with direct layer citations.
- [ ] Record which values are platform-system-owned versus customizable by the integrator.
- [ ] Verify icon/light-dark variants in the template library and sample payloads.
- [ ] Do not claim design accuracy until Figma inspection and HyperOS 3 test rendering are complete.

Source: https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144
