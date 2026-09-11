# Detailed content and modular layout

Current override: Read [Product identity and MiBA layout](identity-and-miba-layout.md) first. Its fidelity and primary layout rules take precedence over conflicting older guidance below.

## Reference and scope

Before writing, read the user's supplied product-detail layout reference if accessible. Otherwise use the [bundled snapshot](product-detail-layout-source.txt) and state that a snapshot was used. It contains S1–S9 wireframes, not product copy or mandatory fields. The mappings below are product-page interpretations and suggestions, not explicit requirements quoted from those wireframes.

## Content before layout

Build `evidence.content_plan` first. For every module, record the buyer's question, verified facts/image sources, points to develop in English, layout type, and purpose of the newly generated imagery. Map source information comprehensively rather than extracting only a title, a few selling points, and a table.

- The overview explains what the product is, who it serves, and its supported distinctions.
- Structure/material/component sections explain how facts affect use or selection, showing real connections and configurations. Do not infer untested durability from material alone.
- Function/benefit sections explain capabilities, uses, and conditions. Avoid unsupported claims such as “high quality” or “more efficient.”
- Operation/compatibility/selection sections explain verified use, variant differences, input requirements, included accessories, and limitations. Do not invent safety or technical procedures.
- Applications combine independent scene images with explanations of the setting and visible advantages, rather than only a generic desktop image and heading.
- Specifications preserve complete units, meaningful differences, and configuration relationships. Repeated values may be consolidated in a table.
- Packaging, customization, delivery, and quality sections use source facts with explicit subjects and conditions. Supplier capabilities do not automatically belong to the user's brand.
- Six FAQs address additional purchasing questions instead of repeating entire preceding paragraphs.

There is no fixed word count. Judge completeness by source coverage and decision value. Record limited source information honestly; do not invent certifications, customers, outcomes, or specifications to fill space. Keep conflicts, production methods, and verification conclusions in evidence/review. Omit unsupported selling points and unresolved values from customer-facing specifications. State clear facts naturally and express purchasing limitations as concise selection guidance.

## Mapping wireframes to content

| Reference | Layout meaning | Optional content |
| --- | --- | --- |
| S1 | Two large side-by-side blocks | Product overview: original main visual plus value statement/key facts. |
| S2 | Four columns by two rows of cards | Supported functions, components, or selection points, each with a heading and informative short copy. |
| S3 | Two alternating two-column rows | Structure, operating states, or technical details with alternating text/image placement. |
| S4 | Three columns by two rows of cards | Applications and benefits; reduce the count when evidence is limited. |
| S5 | Two large columns | Scene plus usage conditions, or specifications and configuration explanations. |
| S6 | Three-column content followed by four-column content | Main applications/configurations and supplementary components; adapt counts to the facts. |
| S7 | Multiple card groups | Customization, packaging, or quality-control processes; avoid crowding and meaningless empty slots. |
| S8 | Vertical full-width entries | Specifications, buying guidance, or six FAQs; the FAQ count remains six. |
| S9 | Mixed full-width, two-column, and localized text/image blocks | Rhythm and grouping for a long page; do not mechanically reproduce every empty box. |

Subject to the primary MiBA layout reference, possible combinations include: two-column overview → key features → alternating details → specifications/compatibility → applications → packaging/customization/quality → company profile → three fixed image blocks → six final FAQs. Merge or omit unsupported modules. Where appropriate, combine two-column, card, and full-width layouts rather than repeatedly stacking a paragraph and image. Using all nine wireframes or filling eight feature cards is not required.

## Responsive and visual requirements

- Use a shared 1400px maximum width, centered on wide screens and 100% wide on mobile. Scope authored selectors to `.xb_import_v2`.
- Suggested image/text ratios are 1:1 or 5:6. Preserve a sensible mobile reading order; do not use visual CSS reordering that conflicts with semantic order.
- Where cards are appropriate, use three or four columns on desktop, two on tablets, and generally one on phones. Short specification cards may use two columns if text remains readable.
- Use `minmax(0,1fr)` for grids, explicit image aspect ratios and width/height, consistent spacing and typography, and restrained accent colors. Do not bake essential text into images.
- Keep image roles separate: CSV cover/gallery assets are not reused in `content`. Generate separate detail visuals, close-ups, and scenes as needed. Do not impose an arbitrary one- or two-image cap or force every card to have an image.
- Prioritize accurate product structure and plausible use. Label illustrative scenes briefly when needed, for example `Desk setup illustration.` Do not imply on-site photography or publish generation methods and reference-source explanations.
- The three fixed blocks after the product body and company profile remain exact heading + supplied image converted to WebP, in their required order. Do not turn them into cards or alternating layouts. The six FAQs follow them.
- Inspect the full page at 1920px and 390px, especially tables, card wrapping, stacked content, and fixed assets. Record `content_richness_reviewed` and `layout_reference_reviewed`; the script cannot judge writing depth or visual quality.

## Manual delivery review

Every purchasing-relevant source fact has a destination or a justified exclusion. Each module adds information. Buyers can understand the product, configuration, and use conditions. Generated images match the copy. The cover and at least four gallery images are distinct, newly generated, and individually reviewed. Record generation provenance and per-image review conclusions in evidence/review; changing `generated=true` is insufficient.

## Current section constraints

These override the older wireframe suggestions above. Set outer left/right section padding to zero on desktop and mobile, retaining appropriate vertical spacing. Section headings are bold, centered H2s. Two columns may hold an image and a complete text block, or independent topics; never split one paragraph across columns or use `column-count` to distribute it. Long paragraphs remain continuous and wrap naturally, without being cut in half for visual balance.

Check horizontal padding, centered H2s, and paragraph continuity at 1920px and 390px.
