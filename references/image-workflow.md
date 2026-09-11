# Images: accurate products, original details, plausible applications

Current override: Read [Product identity and MiBA layout](identity-and-miba-layout.md) first. Its fidelity and primary layout rules take precedence over conflicting older guidance below.

## Separate image roles

- Cover/gallery: generate all images with imagegen using real source product images as references. Each product needs one cover and at least four gallery images; the cover does not count toward the four. Each must be a distinct output, not a duplicate, trivial recoloring, or crop used to meet the count. Use 800×800, a clean background, and the complete subject without stretching or cropping important parts.
- New detail images: generate with imagegen from verified product appearance. Use the corresponding Alibaba image for identity, operating state, and factual purpose. Redesign composition, setting, palette, subject placement, and information layout; changing only the background or text is insufficient. Do not copy unsupported promotions.
- Application scenes: show a supported, plausible use of the product. Generate at least one scene for both `scenario_image` and a relevant detail section, at least 1200px wide.
- Three fixed images: use the specified PNGs under [Fixed blocks](fixed-blocks.md), with role `supplied_static`. Preserve all content and original proportions; do not recreate them with imagegen.

Mark newly generated images by their actual role, cover/gallery/detail/scenario, with `generated=true`. Only the three supplied_static assets have `generated=false`. This records provenance; it does not replace review. Do not fabricate certificates, customer projects, or factory scenes. When needed to distinguish a scene from photography, use a brief natural caption such as `Desk setup illustration.` Keep generation methods, reference frames, and fidelity checks in internal reports. Retain numbers only when verified from legible labels, and check that imagegen has not added or altered text. If structure is inaccurate, retry with a simpler scene; if it remains unreliable, block the asset rather than substituting a source image.

## Image prompt skeleton

```text
Create an original application visualization of the referenced [verified product].
Preserve its actual [shape/material/connections/package proportions] faithfully.
Show it in [supported application] with physically plausible installation or use.
Preserve the referenced product geometry, observed state and factual information purpose.
Create an independent composition, setting, palette and information hierarchy; do not copy the source visual template or merely replace its text/background.
Use MiBA when branding is shown. Do not inherit supplier/example brands or invent a physical logo imprint; not every image needs a logo.
Do not invent specifications, certifications,
customer projects, labels or performance evidence. [Target aspect ratio and dimensions].
```

## image-plan.json

Resolve `source` relative to the plan file. Use descriptive English file names and extensionless `name` values. Each product row has its own plan, whose order determines display order. The example below shows selected roles only; a complete plan also requires at least four gallery entries with `generated=true`.

Before generation, record each image's role, reference, verified structure, distinct view/state, information purpose, and prompt in `image_plan`. A clear three-quarter view is suitable for the cover. Choose gallery images from observed front/side/rear views, connections, open/folded states, or other verified configurations. When evidence is limited, use a known view in a new composition rather than guessing ports, dimensions, accessories, or variants. Generate a separate set of useful detail visuals; do not use one file in both gallery and detail. Record actual imagegen output paths and prompts. `generated=true` cannot replace real tool use and per-image visual review.

```json
{
  "images": [
    {"source": "staging/cover.png", "name": "product-white-background", "role": "cover", "generated": true},
    {"source": "staging/application.png", "name": "product-application-concept", "role": "scenario", "generated": true, "width": 1200},
    {"source": "staging/detail.png", "name": "product-detail-concept", "role": "detail", "generated": true, "width": 1000}
  ]
}
```

`prepare_images.py` uses Pillow for dimensions, format conversion, and compression; it does not generate images. The output directory contains only WebP files, with `<folder>.image-manifest.json` beside it. Compression starts at quality 82/method 6. Cover/gallery/detail images may be reduced to quality 70 to approach 100 KB, without sacrificing readability solely to meet that target. Review files exceeding 100 KB and document acceptance reasons. If quality is inadequate, prepare them again in a fresh output location with `--min-quality 82`. Application scenes prioritize clarity and have no mandatory 100 KB cap. Do not silently discard animation frames; select an appropriate still explicitly first.

After upload, reconcile each local image with its Direct URL, role, dimensions, and alt text. Important images need distinct alt text matching their content. The first visible main image uses `loading=eager`; other images may use `lazy` according to position. Set width/height to prevent layout shifts. Record site-level responsive derivatives/srcset requirements as deployment checks; do not invent URLs for nonexistent sizes.

## Separate CSV gallery and detail images

- cover/gallery: populate CSV `images`; cover also populates `thumb`.
- detail: use only in `content`, never CSV `images`.
- scenario: populate `scenario_image` and `content`, never CSV `images`.
- supplied_static: use only in the three fixed blocks in `content`, never CSV `images`.

Retain every role in the local image manifest and upload manifest. Detail images still need uploading even though they are excluded from `images`. Do not reuse a detail URL as a cover/gallery entry. The 1400px value limits the HTML display container; it does not require every source image to be resized to 1400px. Preserve fixed-asset dimensions and legibility under their dedicated rules.
