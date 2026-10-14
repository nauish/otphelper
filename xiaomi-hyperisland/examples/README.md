# HyperOS 3-only integration examples

- **`package-delivery.json`** is a clean, syntactic demonstration using approved **big summary template 2** (A Image/Text 1 + B Text), **small summary style 1** (icon) and **expanded template 10** (Text 2 + Recognition Graphic 1 + Button 3). It contains documented `param_v2`, `param_island`, `baseInfo`, `picInfo` and `hintInfo` properties and demonstrates a `miui.focus.action_track` action reference. This is **not** Xiaomi business approval or device-rendering certification; replace `APPROVED_BUSINESS_CODE` with a genuinely approved code.
- **`HyperIslandPublisher.kt`** is an illustrative Android/Kotlin publisher that uses stable ID, `Notification` + `miui.focus.param`, local picture/`Notification.Action` Bundles and explicit lifecycle cleanup. You must provide `ic_notification`, `ic_box` and an actual secure `contentIntent`. An ordinary notification is used when the island protocol or permission/approval path cannot be established. **Not compiled or device tested** in this package.
- **`MiPushServerExample.java`** is a backend-only authorized MiPush example; uses a secret from server storage, valid registration ID and matching order sequence. **Not compiled with a live MiPush SDK** in this package.
- **`ride-eta-design.json`** is a UX proposal for *HyperOS 3 only*: big summary 7, small summary 1, expanded 4 and four states.

## Run structural checks

```bash
python scripts/validate_payload.py examples/package-delivery.json \
  --big-template 2 --small-template 1 --expanded-template 10 \
  --picture miui.focus.pic_box --action miui.focus.action_track
python scripts/validate_design_spec.py examples/ride-eta-design.json
python -m unittest discover -s scripts -p 'test_*.py' -v
```

Do not ship without choosing an eligible service scenario, Xiaomi approval, proper secret management, light/dark icons and on-device HyperOS 3 rendering tests. See [official template matrix](../references/official-template-catalog.md), [JSON component fields](../references/hyperos3-component-schema.md), and [official Figma source](../references/figma-design-reference.md).
