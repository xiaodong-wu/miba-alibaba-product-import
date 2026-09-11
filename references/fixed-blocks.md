# Three image-only blocks before the final FAQ

No legacy HTML template is required. After the English product body and fixed company profile, insert the following three blocks in this exact order, then the six FAQs at the bottom of the complete detail. Derive headings from original filenames without extensions, preserving capitalization and spaces:

| Order | H2 heading | Bundled file, relative to the skill directory | WebP filename |
| --- | --- | --- | --- |
| 1 | Factory Photo | `assets/fixed-blocks/Factory Photo.png` | factory-photo.webp |
| 2 | MiBA Logo Options | `assets/fixed-blocks/MiBA Logo Options.png` | miba-logo-options.webp |
| 3 | MiBA Accessory Options | `assets/fixed-blocks/MiBA Accessory Options.png` | miba-accessory-options.webp |

Read the named files directly from the skill's `assets/fixed-blocks/` directory. Do not search unrelated local directories or request another upload. If a file is absent, report a missing skill asset. Only convert to WebP and compress reasonably, preserving the full image, original pixel dimensions, aspect ratio, and text. Do not change brands, crop, or regenerate with AI. These assets are exempt from the new-detail-image generation requirement; their presence does not require a MiBA mention in every sentence.

Each block contains only `section > h2 + img`: no paragraphs, captions, lists, or buttons. Use the heading as alt text, actual dimensions as width/height, and `loading=lazy`. Images span the responsive detail container, whose maximum width is 1400px, without changing their proportions. Do not derive displayed headings from compressed filenames.

Append these three objects after the product images in each product's image-plan array. Replace `<skill-dir>` with the current skill directory's absolute path, not a desktop path or the task working directory:

```json
[
  {"source":"<skill-dir>/assets/fixed-blocks/Factory Photo.png","name":"factory-photo","role":"supplied_static","generated":false},
  {"source":"<skill-dir>/assets/fixed-blocks/MiBA Logo Options.png","name":"miba-logo-options","role":"supplied_static","generated":false},
  {"source":"<skill-dir>/assets/fixed-blocks/MiBA Accessory Options.png","name":"miba-accessory-options","role":"supplied_static","generated":false}
]
```

`prepare_images.py` records source filenames, SHA-256 hashes, headings, and output dimensions. Upload the WebP files normally. Their URLs belong only in fixed blocks in `content`, not CSV `images`; `thumb` and `scenario_image` still use the product cover and generated application image. `compose_content.py` uses image/upload manifests to place the blocks before the final FAQ.

Fixed images contain text. Keep the default quality 82 rather than reducing it to meet 100 KB; document a readability exception for larger files. Compare every converted image with its original. HTML `src` values must use uploaded Direct links, not local paths.

Set outer left/right padding to zero, retain suitable vertical spacing, and use bold (700), centered H2 headings.
