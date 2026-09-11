# Miba Alibaba Product Import

A Codex skill that turns Alibaba product links in a CSV import sheet into English product content for MiBA.

It can:

- extract verifiable product titles, specifications, variant details, packaging information, and reference images;
- write independent English product descriptions, six purchasing FAQs, SEO titles, meta descriptions, and file-name slugs;
- generate a new product cover, at least four distinct gallery images, separate detail images, and an application scene with imagegen;
- preserve the product's observed structure, proportions, labels, and connections while creating independent image compositions;
- generate `pro_fields` as four to eight plain lines without leading bullets, dots, dashes, numbering, or the legacy separator;
- insert the supplied company profile, then Factory Photo, MiBA Logo Options, and MiBA Accessory Options, with all six FAQs at the bottom;
- create responsive product details with a centered 1400px maximum width and bold, centered H2 section headings;
- convert images to WebP, upload them to ImgBB, and populate the CSV with Direct links;
- preserve source links, API-key values, unknown columns, and row order;
- validate the completed CSV, local assets, upload manifests, and review records before delivery.

MiBA is the target website brand. Source supplier qualifications, certifications, and company capabilities must not be presented as MiBA's own. The bundled company profile remains verbatim user-supplied content.

## Install with Codex

Ask Codex:

```text
Use $skill-installer to install the skill at the root of this repository
with the name miba-alibaba-product-import:
https://github.com/xiaodong-wu/miba-alibaba-product-import
```

Or run the bundled installer directly:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo xiaodong-wu/miba-alibaba-product-import \
  --path . \
  --name miba-alibaba-product-import
```

The skill lives at the repository root. The installation destination must not already exist; back up an existing installation before replacing it. The skill becomes available on the next Codex turn.

The helper scripts require Python 3.10+ and [Pillow](https://pypi.org/project/pillow/). Install the dependency from the repository root:

```bash
python3 -m pip install -r requirements.txt
```

The complete workflow also needs browser access to Alibaba, imagegen, and an ImgBB API key supplied in the input CSV. The Python scripts handle preparation, upload, composition, and validation; they do not browse product pages or generate images themselves.

## Use

```text
Use $miba-alibaba-product-import to process this Alibaba product import CSV.
```

Provide a CSV containing `link` and `IMGBB_API_KEY` for each product. The [blank import template](assets/content_import_template.csv) provides the headers. An existing `template` column is preserved but not used to generate the new detail.

The skill preserves the source file and writes `<input-stem>_completed.csv`. Final WebP files are saved under `images/<file_name>/` beside the output table, with evidence, image/upload manifests, and review/validation reports.

Each product gallery contains one cover and at least four gallery images. Detail, application, and supplied fixed images are separate from CSV `images`. The final detail order is:

```text
English product body
Company Profile
Factory Photo
MiBA Logo Options
MiBA Accessory Options
Six FAQs
```

The workflow follows the bundled [product optimization requirements](references/google-product-seo-requirements.md), an English translation of a user-provided specification snapshot. It is not an automatically updated Google policy library or a guarantee of indexing or rankings.

## Repository layout

```text
miba-alibaba-product-import/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── company-profile.html
│   ├── content_import_template.csv
│   └── fixed-blocks/
│       ├── Factory Photo.png
│       ├── MiBA Logo Options.png
│       └── MiBA Accessory Options.png
├── references/
│   ├── schema-and-workflow.md
│   ├── source-coverage.md
│   ├── content-layout.md
│   ├── image-workflow.md
│   ├── identity-and-miba-layout.md
│   ├── fixed-blocks.md
│   ├── company-profile.md
│   ├── google-product-seo-requirements.md
│   └── product-detail-layout-source.txt
├── scripts/
│   ├── prepare_images.py
│   ├── upload_images_to_imgbb.py
│   ├── compose_content.py
│   ├── validate_output.py
│   └── test_workflow.py
├── requirements.txt
└── LICENSE
```

The commands below run from the repository root. When using an installed skill from another working directory, replace `scripts/` with the absolute path to that installation's scripts directory.

## Prepare images

Generate and visually review product images with imagegen first. Create an image plan using the roles documented in [Image workflow](references/image-workflow.md), including the three supplied fixed assets described in [Fixed blocks](references/fixed-blocks.md).

```bash
python3 scripts/prepare_images.py \
  /absolute/path/to/image-plan.json \
  --output-dir /absolute/path/to/images/product-slug
```

Cover and gallery images become 800×800 WebP. Application scenes must be at least 1200px wide. Compression starts at quality 82 and method 6, with readability taking priority over the approximate 100 KB target. Fixed assets retain their original pixel dimensions, content, and proportions; they are converted, not regenerated. Use a fresh output directory and manifest path for each preparation run.

## Upload images to ImgBB

Add the ImgBB API key to `IMGBB_API_KEY` in each populated CSV row. The uploader reads that field directly and never prints the value or writes it to the upload manifest.

```bash
python3 scripts/upload_images_to_imgbb.py \
  /absolute/path/to/images/product-slug \
  --csv-file /absolute/path/to/input.csv \
  --row-number 2 \
  --manifest /absolute/path/to/upload-manifests/product-slug.json
```

The uploader uses [ImgBB API v1](https://api.imgbb.com/), enforces the 32 MB limit, and records only WebP `data.url` Direct links. Keys and delete URLs are excluded from the manifest. `--row-number 2` means the first product record after the header, regardless of embedded newlines in CSV cells.

Populate a row's image fields only after all required uploads succeed. Preserve and inspect a partial manifest before retrying; the uploader does not resume automatically. Input and completed CSVs retain API keys and must not be committed to GitHub or shared as public examples.

## Compose product details

Author the product body and a final section marked `miba_faq_section` containing six `xb_faq_item` entries. The composer inserts the fixed company profile and three ordered image blocks, then places the FAQ last.

```bash
python3 scripts/compose_content.py \
  --detail-file /absolute/path/to/product.detail.html \
  --image-manifest /absolute/path/to/images/product-slug.image-manifest.json \
  --upload-manifest /absolute/path/to/upload-manifests/product-slug.json \
  --output /absolute/path/to/content.html
```

The composer requires completed uploads and a fresh output file. It produces an HTML fragment; use a CSV-aware writer to populate `content` and the other generated fields.

## Validate

Record completed factual, coverage, image, layout, and visual checks in `review.json`, following [Fields and workflow](references/schema-and-workflow.md). Review the complete detail at desktop and mobile widths before marking visual checks as passed.

```bash
python3 scripts/validate_output.py \
  /absolute/path/to/input.csv \
  /absolute/path/to/input_completed.csv \
  --images-dir /absolute/path/to/images \
  --review /absolute/path/to/review.json \
  --report /absolute/path/to/validation.json
```

Keep `upload-manifests/` beside `images/`. Exit code `0` means local validation passed without skipped or blocked rows, `2` indicates a partial result, and `1` indicates validation errors. Report deployment checks separately: local validation does not certify live CMS headings, canonical URLs, indexing, or Core Web Vitals.

Run the offline workflow tests from the repository root:

```bash
python3 -m unittest discover -s scripts -p test_workflow.py -v
```

These tests do not perform live Alibaba extraction, image generation, or ImgBB uploads.

## License

Released under the [MIT License](LICENSE). The uploader is based on MIT-licensed code from [Xinbada Alibaba Product Import](https://github.com/xiaodong-wu/xinbada-alibaba-product-import); see [source attribution](references/schema-and-workflow.md#source-attribution).
