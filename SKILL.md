---
name: miba-alibaba-product-import
description: Convert Alibaba product CSVs into English product imports for MiBA. Generate a new cover, at least four gallery images, detailed product content, application imagery, a fixed company profile and three supplied image blocks before six final FAQs. Convert images to WebP, upload to ImgBB, and validate the completed CSV. Use for MiBA import sheets containing a link column.
---

# Miba Alibaba Product Import

Workflow: user CSV and Alibaba links → verified product facts and reference images → newly generated cover, gallery, detail and application images → English product copy → WebP conversion and ImgBB upload → company profile, three fixed image blocks and final FAQs → completed CSV → validation and delivery.

## Required references and precedence

Read and apply the bundled [Google product optimization requirements](references/google-product-seo-requirements.md). Read [Fields and workflow](references/schema-and-workflow.md) for the CSV and delivery contract.

The user's current instructions take precedence. Apply the bundled content, SEO, image and page requirements. Use MiBA as the target website brand; do not introduce other websites' brands, company names or unrelated product examples into generated content. Product specifications must come from verified information about the current product. Do not attribute the source supplier's qualifications, certifications or company capabilities to MiBA. Preserve the user-supplied company profile verbatim.

No legacy HTML template is required. The final order is: English product body → Company Profile → Factory Photo → MiBA Logo Options → MiBA Accessory Options → six FAQs.

Before generation, read [Product fidelity and MiBA layout](references/identity-and-miba-layout.md). Use original Alibaba images to verify product structure while designing independent compositions. Follow the user's latest layout requirements. Write SEO titles and descriptions independently; they need not equal the product title and summary.

## Detail layout requirements

These rules override conflicting examples in the layout references:

- Set every section's outer left and right padding to zero, including the overview, body, company profile, fixed images and FAQ, on desktop and mobile. Retain suitable vertical spacing: approximately 28–40px on desktop and 20–28px on mobile. Internal spacing such as table-cell padding is allowed.
- Keep each paragraph in one continuous text block. Do not split it into left/right columns or use CSS multicolumn flow. Images may sit beside complete text blocks, and independent topics may appear side by side. Stack them naturally on narrow screens.
- Use `<h2>` with `font-weight:700;text-align:center` for section headings. Do not substitute H3, plain divs or inline bold text. Inline labels and individual FAQ questions are not section headings.

## Workflow

### 1. Check the input and fixed assets

Preserve the source CSV and default to `<input-stem>_completed.csv`. Check `link` and `IMGBB_API_KEY` for each row. Preserve row order, protected source values and unknown columns. Only the upload script reads keys; do not print complete rows or tables, log secrets, or commit CSVs containing keys.

Copy the user's uploaded or specified CSV into the task output directory before processing. If no CSV was supplied, ask for an import sheet containing an ImgBB key. The [blank header template](assets/content_import_template.csv) defines the field structure. Preserve an existing `template` column without using its content.

Use these bundled files for the fixed image blocks:

| Order | Section heading | Bundled image |
| --- | --- | --- |
| 1 | Factory Photo | `assets/fixed-blocks/Factory Photo.png` |
| 2 | MiBA Logo Options | `assets/fixed-blocks/MiBA Logo Options.png` |
| 3 | MiBA Accessory Options | `assets/fixed-blocks/MiBA Accessory Options.png` |

If a bundled file is missing, report the missing skill asset. Do not replace it with an AI-generated image.

### 2. Extract source information and search intent

BrowserAct preference: inspect connectable existing browsers and tabs first. Prefer the user's ordinary browser and existing login session. Open new product links in ordinary tabs there; do not proactively use incognito/private mode or isolated temporary contexts. Do not overwrite or close the user's existing tabs. Keep a visible window for manual verification and continue in the same tab afterward. If no browser can be reused or connected directly, a new visible ordinary window may be opened within the user's authorization. Do not close or restart their active Chrome without authorization. State any session-reuse limitation accurately; do not describe an isolated session as reused. The user has requested that the Codex in-app browser not be used, so do not automatically fall back to it.

Read [Source coverage](references/source-coverage.md). Use as much accessible, verifiable information relevant to buying decisions as the current product link provides. Do not write a short generic description from only the title and first screen. Expand specifications and descriptions, scroll to load relevant images, and inspect variants, packing and delivery information. Record what was extracted, where it was used, why it was excluded, and which areas could not be accessed.

Read the current Alibaba page and gallery with an available browser. Extract verifiable titles, specifications, materials/formulas, structure, uses, packaging and certification information. Preserve numbers and units. Prefer specification tables for conflicting product attributes and legible labels for serving/nutrition information. Record unresolved conflicts instead of guessing.

Write one local evidence JSON per row: source URL, access time, facts with visible text/image references, coverage inventory, each fact's destination section or exclusion reason, one primary keyword, two to five long-tail keywords, missing information and conflicts. Never reuse another product's facts. If the page cannot be accessed, skip the row and record why; do not invent missing specifications.

### 3. Write the product detail

Read [Fixed company profile](references/company-profile.md). Insert the user-supplied company copy verbatim after the product body, followed by the three specified image blocks and the final FAQ. The composer reads `assets/company-profile.html`; do not duplicate this text in the authored product body. Its company capabilities and commercial terms come from supplied copy and must not automatically become product-specific specifications, configurations or delivery promises.

Write for buyers: explain supported structure, functions, uses and choices directly. Do not publish evidence records, review comments, AI production methods or lists of unverified supplier claims as selling points or captions. Omit unsupported protocols, certifications, protection features and magnet grades, recording the reason internally. Removing a disclaimer does not make an unsupported claim valid. Retain purchasing conditions such as compatible models, power requirements and included accessories as concise product or configuration information. Review the body, tables, captions, FAQs, SEO fields and alt text separately for customer relevance.

Read [Content and layout](references/content-layout.md), then the user's supplied layout reference if accessible; otherwise use the [bundled layout snapshot](references/product-detail-layout-source.txt) and state that a snapshot was used. Its S1–S9 wireframes are structural examples. Select side-by-side, alternating and multicolumn arrangements according to the evidence; do not mechanically fill all nine patterns.

Develop verified structure, functions, operation, compatibility, selection, applications, packaging and customization using fact → purchasing significance → use conditions. A short overview, a table and repeated requests to confirm details do not constitute a complete page. Do not inflate length with paraphrases, repeated FAQs, unsupported benefits or invented cases. Build `evidence.content_plan` before writing. Keep source discrepancies, verification steps, unsupported claims and exclusion reasons in evidence/review. Do not publish unresolved values as definite specifications; express material limitations as concise selection guidance.

Apply the optimization document's keyword, metadata, image, content, page-experience and acceptance requirements. Write independent English copy rather than translating Alibaba or legacy template text sentence by sentence.

Begin with an overview, then organize supported introductions, specifications, benefits, applications, actual cases or illustrative scenes, packaging/delivery, certifications, factory capabilities, company advantages and six purchasing FAQs. Suggested sections do not justify invented facts. Omit unsupported certifications or cases; flag missing lead times for confirmation. Use company names and OEM/ODM capabilities only when supplied by the user or verifiable in the current source, without assuming they belong to the target company.

The full product page must have exactly one main H1, supplied by the outer product title. A standalone preview places its H1 outside the detail container. Mark unknown CMS heading behavior as pending deployment verification. Use centered bold H2 headings throughout the detail. Keep the six FAQs as the last content section, after the company profile and all three fixed image blocks.

The complete detail, including fixed blocks and FAQ, has a responsive maximum width of **1400px**, centered on wide screens and 100% width on narrow screens. Do not use a fixed 1400px width. `compose_content.py` adds the shared outer container. Keep internal content within it, images at `max-width:100%;height:auto`, and table overflow inside the table's own container. Avoid `100vw`, oversized minimum widths and absolute positioning that expands the page. Namespace authored content and CSS under `.xb_import_v2`. Set explicit image width/height and responsive styles. Output an HTML fragment only: no html/head/body wrappers, external fonts, global CSS, executable JavaScript or meta keywords. Put SEO metadata in CSV fields, not the detail HTML. Structured data is a site-integration concern; never fabricate ratings, prices or stock.

Place the six `xb_faq_item` elements in a separate `<section class="xb_import_v2 miba_faq_section" style="padding:26px 0">` at the end of the authored detail. Only closing wrapper tags may follow it. The composer moves this section after the fixed blocks. Do not mix the FAQ into the product body.

Save the authored fragment as `<file_name>.detail.html`. After all uploads succeed, run `scripts/compose_content.py` to insert the company profile and fixed images, place the FAQ last, and produce final `content`. Each fixed image block contains exactly one H2 and one image, with no extra introduction, caption, button or other content.

### 4. Generate and prepare images

Original Alibaba gallery and detail images must be imagegen inputs for product identity, function and use, not templates for copying the composition. Lock the observed silhouette, proportions, parts, materials, ports and device contact. Substantially redesign framing, subject placement/scale, setting, props, lighting, palette and information hierarchy. Merely recoloring the background, replacing text or moving a few elements is insufficient. Do not copy distinctive effects, giant numeral backgrounds, arrow combinations or thumbnail grids. Retain supported viewing angles without inventing unseen parts to reduce resemblance. Record `identity_locks` and `design_changes` separately before generation; assess fidelity and visual independence separately afterward. The user's earlier “80% similarity” comment criticized excessive resemblance; it is not a target or a measured metric. Do not invent similarity scores or promise fixed percentages. Do not reproduce unsupported promotional claims.

Read [Image workflow](references/image-workflow.md). Generate every product cover, gallery image, detail illustration and application scene with imagegen using inspected source references. Do not pass source files off as generated results. Use targeted reference-image generation that preserves the product while substantially redesigning the surrounding composition. Generate one distinct cover and at least four distinct gallery images per product: at least five entries in CSV `images`. The cover, detail images, scene and fixed assets do not count toward the four gallery images. Show supported differences in angle, structure, state or color; do not pad the count with renamed duplicates or trivial variations. The three supplied fixed images are the exception: convert their bundled PNGs to WebP without regeneration, text changes, cropping or content changes.

Preserve verified product geometry, connections, proportions and labels. When an illustrative scene must be distinguished from photography, use a brief natural caption such as `Desk setup illustration.` Do not imply a real customer project or factory visit. Keep image-generation methods, source-frame provenance and proportion checks in internal records, not product copy.

Use MiBA for displayed branding, never a supplier/example brand. A logo is not required on every image, and the website brand does not establish a physical logo imprint. Use user-supplied MiBA assets when a brand mark is requested, process them with imagegen as instructed, and verify other labels and numbers remain accurate. Do not invent unseen rear structures or accessories to complete the gallery count. After reviewing each image, prepare the role manifest and run `scripts/prepare_images.py`: cover/gallery are 800×800, scenario width is at least 1200px, and detail dimensions follow the layout. Start WebP compression at quality 82 and method 6. Preserve fidelity; review and document size exceptions.

### 5. Upload and populate the CSV

Use the bundled uploader with the `IMGBB_API_KEY` from each CSV row; never pass plaintext keys on the command line. Populate image fields only after all images required for that row upload successfully. The uploader retries network, 429 and 5xx errors a bounded number of times. Record persistent failures instead of retrying indefinitely. Retain partial success manifests and inspect them before retrying; the script does not provide resume support.

Set `thumb` to the cover and `scenario_image` to the new application image. **CSV `images` contains only cover/gallery assets**, in manifest display order: cover first, then at least four gallery images, one `<url>|<English alt>` entry per line. Exclude detail images, scenes and all fixed assets. Detail images appear only in `content`; the scene also populates `scenario_image`. Do not add detail images to satisfy an obsolete validator.

`pro_fields` contains four to eight verified product attributes, one `Field:Value` entry per line in the CSV cell. Use an English field name and an ASCII colon (`:`), with a nonempty value; a space after the colon is optional. Do not write standalone selling-point sentences, leading bullets, dots, dashes, numbering or legacy separators. Follow the format example in [Fields and workflow](references/schema-and-workflow.md#pro_fields), using only attributes and values supported for the current product.

Convert and upload every image role and retain all files in local and upload manifests. Populate fields only with the returned `data.url` Direct link in the form `https://i.ibb.co/...webp`. Resolve `content` images from uploaded detail/scenario/supplied_static records; they need not appear in CSV `images`. Preserve the exact fixed headings, assets and order.

### 6. Validate and deliver

Record row status and completed manual checks using [Fields and workflow](references/schema-and-workflow.md), then run:

```text
python scripts/validate_output.py input.csv input_completed.csv --images-dir images --report validation.json --review review.json
```

Fix all errors for successful rows. Reconcile the source coverage inventory so useful accessible specifications, explanations and image information are accounted for. List inaccessible areas honestly rather than claiming complete extraction. Visually inspect the combined English detail, company profile, fixed images and final FAQ at mobile (for example, 390px) and wide desktop (1920px) widths. Confirm the 1400px maximum, no page-level horizontal overflow, accurate products and labels, sound geometry, appropriate scene captions and supporting source evidence. The script does not establish search indexing, image originality or factual truth.

Deliver the completed CSV, local WebP files, upload manifests, evidence and validation report. State the number of successful, skipped and blocked rows; label any skipped/blocked result as partial. Preserve the source key column, so return completed CSVs containing keys only to the user, never as public examples. Without a deployment environment, mark canonical URLs, redirects, internal links, Sitemap, robots, hreflang, image HTTP access and Core Web Vitals as unverified. Do not claim they passed or publish the site without authorization.
