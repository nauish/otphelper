# Source index and confidence for the HyperOS 3-only Skill

**Reviewed:** 2026-10-14. Output is an English technical interpretation; Xiaomi's current developer documentation and approval decisions control real production use.

## Official Xiaomi developer sources

1. [Xiaomi Super Island service](https://dev.mi.com/xiaomihyperos/ability/XiaomiHyperIsland): service concept, scenario eligibility and enrollment.
2. [Development Guide](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2131): `miui.focus.param`, `param_v2`, Android Notification, MiPush and resource Bundles.
3. [Onboarding & approval](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2132): service/certificate registration, whitelist, scene review and release entitlement.
4. [Version Information](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2141): verify the HyperOS 3 runtime gate. This Skill intentionally documents only the HyperOS 3 path.
5. [Summary-state templates](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2143): 9 big-island arrangements, 3 small-island modes, icon/picture sizes, copy rules and character-capacity PDF.
6. [Expanded-state templates](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2142): official template IDs, approved component combinations, asset and progress drawings. Page update displayed as 2026-01-29.
7. [UX proposal and editable Figma file](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2144): official `.fig` design reference, editable `.docx` proposal, UX review rules and timeout guidance.
8. [Super Island FAQ](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2146): payload byte budget, permission, image limits and timeout units.
9. [Media drag sharing](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=2162): special media and drag/share extension semantics. Implement only if your selected approved business scene requires it.

## User-supplied converted official library (field extraction)

- `小米超级岛模板库20260129.md`: uploaded Markdown conversion of **Xiaomi Super Island Template Library dated 2026-01-29**, about 1,920 source lines. It contains detailed expanded/summary component JSON tables and layout notes. The converted file is **not bundled verbatim** because it is machine-extracted, has malformed quote characters/OCR and includes material outside this Skill's target platform; instead, the relevant HyperOS 3 fields are reviewed and translated in [hyperos3-component-schema.md](hyperos3-component-schema.md).
- **Known mismatch:** converted late expanded templates are numbered `15`–`21`, while the live official expanded guideline uses `16`–`22`. Use the live official numbering, and report this discrepancy in [official-template-catalog.md](official-template-catalog.md).
- **Other conversion uncertainties:** `timerCurrent` vs `timerSystemCurrent`, `animIconInfo.type: 3` example vs `type: 0` table, potentially mistyped asset prefix `miui.land.pic_`, `booean` field type, and corrupted quotation marks. All require runtime/source verification before claiming renderability.
- The **official 3-page character-capacity PDF** was previously independently inspected; its translated guidance is [island-text-capacity.md](island-text-capacity.md). Original PDF is linked there.
- The official **Figma `.fig` source** is linked on Xiaomi's proposal page. It was **not** downloaded or inspected as a binary here. See [figma-design-reference.md](figma-design-reference.md).

## Community/unofficial wrappers

- [D4vidDf HyperIsland ToolKit](https://github.com/D4vidDf/HyperIsland-ToolKit), [docs](https://hyperisland.d4viddf.com/docs/getting-started/): third-party Kotlin builder, not a Xiaomi-maintained SDK.
- [HuberHaYu Xiaomi-SuperIsland-Playground](https://github.com/HuberHaYu/Xiaomi-SuperIsland-Playground): community playground relying on experimental private/system routes; not Xiaomi production authorization.
- [Alibaba Cloud EMAS vendor guide](https://help.aliyun.com/en/document_detail/3037956.html), [JPush REST API](https://docs.jiguang.cn/en/jpush/server/push/rest_api_v3_push): provider-specific push adapters, not direct Xiaomi API replacements.

## Interpretation rules

- **OFFICIAL**: published Xiaomi developer page; cite its URL.
- **EXTRACTED**: normalized from the user's converted original template library; cite the source name and clearly label uncertainties.
- **DESIGN ADAPTATION**: hypothetical English wireframe/scenario; never call approved/render-tested.
- **COMMUNITY**: source and artifact versions may change; verify latest release, license and actual device behavior.

Recheck official HyperOS 3 developer documents for changes before shipping.
