# Source coverage limited to the current product link

Use as much verified information about the current product as possible. Collect first, then organize; do not write generic marketing copy from the first-screen title alone. Follow the user's product optimization requirements: complete and accurate specifications, independent natural writing, and no copied source prose.

## Collection scope

Read and expand the current product page in an available browser. Scroll to load later content and open specifications, descriptions, and options as needed. Cover these areas where they actually exist:

- Full title, overview, key attributes, and complete specifications: model, dimensions, materials, weight, functions, power, formula, and other relevant facts.
- Options and variants: colors, sizes, configurations, compatible devices/applications, and optional accessories. Preserve variant relationships rather than combining them into one configuration.
- Relevant description text, tables, gallery images, and detail images, including readable dimensions, labels, installation/use instructions, structural features, and limitations.
- Package contents, individual/carton dimensions and weights, packing quantities, shipping protection, delivery, minimum order quantities, samples, and customization requirements.
- Certification/test descriptions, FAQs, usage guidance, and genuinely accessible demonstration-video information on the current page.
- Supplier, production, and quality-control capabilities relevant to the product. Record the responsible entity; do not automatically treat its factory, certificates, or customer cases as the target brand's.
- Visible prices, quantity tiers, shipping costs, stock, promotions, and lead times, with access times and conditions. Without user confirmation, do not convert dynamic supplier quotes or promises into fixed target-site commitments.

Exclude navigation, advertising, recommended products, other products' specifications, personal account information, and irrelevant reviews. Record inaccessible videos, illegible image text, and areas that cannot be expanded. Do not guess or repeat attempts that make no progress.

## Map source information to the detail

Add `content_plan` to the evidence JSON. For each module, record its heading, source facts, buyer question, writing points, S1–S9 layout choice where applicable, required generated images, and omission reasons. Add a `coverage` array with entries such as:

```json
{
  "section": "Packaging and delivery",
  "access": "read",
  "facts": [{"value":"Exact source fact with units", "source":"Visible section/table/image reference"}],
  "used_in": ["Packaging section", "Specification table"],
  "omitted_reason": ""
}
```

Use `read`, `unavailable`, or `not_present` for `access`. For conflicting facts, preserve the competing sources and resolution rationale. Every important collected fact needs a destination or justified exclusion. Do not omit necessary specifications, use limitations, or package configurations merely to be concise. Consolidate duplicates. Exaggerated marketing, supplier identity, and unsuitable dynamic commercial information may remain in evidence with reasons for exclusion from the product body.

Review backward after writing: are all useful source sections accounted for, are numbers and units complete, are variants distinct, are image-only facts represented as crawlable text, and has source information been wrongly turned into a target-company commitment? The six FAQs supplement buying decisions; their count and an arbitrary body length must not limit source coverage.

Use the current link comprehensively while preserving independent writing, factual accuracy, and newly generated detail imagery. Extract useful facts from original images but do not copy full Alibaba detail graphics. The three supplied fixed assets retain their explicit exception.
