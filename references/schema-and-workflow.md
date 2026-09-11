# Fields, workflow, and acceptance contract

## CSV

Preserve original columns, column order, row count, and UTF-8 encoding. Use the CSV module to handle commas, quotes, and newlines in HTML; do not split CSV records by physical text lines. The uploader's `--row-number` is the logical record number including the header: the first product is row 2, regardless of multiline HTML cells.

| Field | Rule |
| --- | --- |
| `link`, `IMGBB_API_KEY` | Preserve the original values character for character; never log keys. |
| Unknown columns | Preserve their original values. |
| `content` | English product body → fixed company profile → Factory Photo → MiBA Logo Options → MiBA Accessory Options → final FAQ, inside one centered responsive container with a 1400px maximum width. |
| `title` | Natural English product heading; use MiBA where it reads naturally, without keyword stuffing. |
| `remark` | One or two sentences describing supported product value. |
| `pro_fields` | Four to eight verified product attributes, one `Field:Value` entry per line, using an English field name, ASCII colon and nonempty value; no leading bullets, dots, dashes or numbering. |
| `file_name` | Short descriptive lowercase letters, digits, and hyphens; no extension; unique per row. |
| `seo_title1` | Independently written English Title Case, 50–65 characters, targeting about 60; primary keyword near the start, MiBA usually at the end; unique per row. |
| `seo_desc` | Independently written, no more than 140 characters, with benefits and uses supported by the body; unique per row. |
| `thumb` | ImgBB WebP Direct URL for the cover. |
| `scenario_image` | ImgBB WebP Direct URL for a newly generated application scene, not Markdown. |
| `images` | One newly generated cover followed by at least four newly generated gallery images, in display order, one `<url>|<alt>` per line. Exclude detail/scenario/supplied_static assets. Use accurate, distinct English alt text. |

The 50–65 character SEO title range is the user's editorial standard, not a mandatory Google limit. All new copy is English. Do not inherit source brands; manually review branding against MiBA and do not attribute supplier qualifications to MiBA. A `template` column is optional; preserve it when present without using its content.

Use the [fixed company profile rules](company-profile.md) and bundled HTML. Preserve the supplied copy verbatim and place it before the three fixed images.

## pro_fields

Write four to eight verified product attributes, each on its own line inside the same CSV cell, in `Field:Value` format. Use an English field name and an ASCII colon (`:`); both the field name and value must be nonempty. A space after the colon is optional. Commas, spaces, quoted text, numbers and units may remain inside values. Separate entries with real newlines, not literal `\n` text or the legacy separator. Do not use standalone selling-point sentences or leading bullets, dots, dashes or numbering.

Format example supplied by the user:

```text
Material:ABS, Fabric
Color:Black
Speaker output:5W
Delivery:FOB,EXW,FCA
Country of Origin: Made in China
```

These lines demonstrate formatting, not mandatory fields or facts for every product. Choose labels and verified values relevant to the current product. Do not transfer the example's fabric material, speaker power, delivery terms or origin to another product without supporting evidence. Delivery terms must apply to the target offer; source supplier terms alone do not establish MiBA's terms.

## File layout and commands

Absolute paths are supported. Relative output paths below assume the task output directory as the working directory; replace `scripts/` with the actual absolute path to the skill's scripts.

```text
input_completed.csv
images/<file_name>/<descriptive-name>.webp
staging/<file_name>/             # Not part of the final gallery
evidence/<file_name>.json        # Sources, facts, keywords, and gaps; no keys
upload-manifests/<file_name>.json
review.json
validation.json
```

```text
python scripts/prepare_images.py image-plan.json --output-dir images/product-slug
python scripts/upload_images_to_imgbb.py images/product-slug --csv-file input.csv --row-number 2 --manifest upload-manifests/product-slug.json
python scripts/compose_content.py --detail-file product.detail.html --image-manifest images/product-slug.image-manifest.json --upload-manifest upload-manifests/product-slug.json --output content.html
```

The composer does not write CSV files. Use `csv.DictWriter` to populate generated content without printing row data to the terminal.

## review.json

Write this record after actually performing the checks. Do not prefill true values as a shortcut. Include every populated row; blank rows do not need records. Use `skipped` for unavailable source pages or insufficient facts, and `blocked` for missing fixed assets, inaccurate image generation, upload failure, or similar execution blockers. A `success` record identifies a candidate that must pass both manual and automated validation.

```json
{
  "rows": [
    {
      "row_number": 2,
      "status": "success",
      "reason": "",
      "checks": {
        "facts_verified": true,
        "source_coverage_reviewed": true,
        "fixed_blocks_verified": true,
        "original_detail_images_verified": true,
        "generated_gallery_verified": true,
        "content_richness_reviewed": true,
        "layout_reference_reviewed": true,
        "visual_review_passed": true,
        "seo_document_reviewed": true
      },
      "evidence": "evidence/product-slug.json",
      "notes": ["Describe the evidence for completed checks; never include keys."]
    }
  ],
  "deployment_pending": ["Verify the CMS H1, canonical URL, image HTTP responses, Sitemap, robots, and real-user Core Web Vitals on the deployed site."]
}
```

The validator checks the 1400px outer container, gallery/detail separation, fields, preserved source values, exact fixed headings/images/order, FAQ/H1 structure, metadata length and uniqueness, image URLs and alt text, local WebP files, and role-specific dimensions. Manually review every optimization requirement, product identity, independent copy, factual evidence, image originality and accuracy, CSS scope, and rendered output. A manual `success` flag cannot override automatic errors. Exit code 0 means local candidates passed without skipped or blocked rows; 2 means partial completion; 1 means validation errors. Always report unverified deployment requirements separately.

The validator reads `upload-manifests/<file_name>.json` from the parent of `--images-dir` and reconciles uploads, local files, image roles, and CSV URLs. CSV `images` is matched only against cover/gallery; content images are matched against the full upload manifest. Do not mix the two sets. Newly generated detail images use `generated=true`. The three supplied fixed images use `supplied_static` and are explicitly exempt from AI generation, but their provenance still requires manual review. Preserve input values in generated fields for skipped/blocked rows; keep drafts outside the import table.

## Source attribution

The uploader is based on MIT-licensed code from `xiaodong-wu/xinbada-alibaba-product-import`, commit `1f5b0cc6b3cbe69dbf1cf9c1641d03c56ac93480`, with support added for large HTML CSV fields. Retain the bundled LICENSE. Other workflow and validation components were rewritten for this task. The bundled Google requirements are an English translation of the user-supplied document snapshot, not an automatically updated official Google rules library.

Follow [Source coverage](source-coverage.md). Set `source_coverage_reviewed` only after an actual item-by-item review. The script checks review flags; it does not prove complete extraction or accurate content. A static 1400px container check does not replace browser layout review.
