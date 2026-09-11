# Fixed company profile

Place the company profile after the product body and before Factory Photo. The complete order is: product body → company profile → Factory Photo → MiBA Logo Options → MiBA Accessory Options → six final FAQs.

Use the fixed content in [company-profile.html](../assets/company-profile.html), inserted exactly once by `compose_content.py`. This is company information supplied directly by the user, not extracted from Alibaba. Do not automatically correct spelling, grammar, punctuation, capitalization, spacing, or wording, including `openning`, `fastly`, `parter`, `Provice`, and `shippment`. Do not replace markets, lead times, payment terms, addresses, or contact details, or regenerate the profile for each product.

Layout, spacing, typography, and responsive presentation may be adjusted; keep link display text unchanged. The layout contains five numbered strengths, mission and markets, shipping/payment columns, and contact information, stacking on mobile. Scope all CSS to `.xb_import_v2.miba_company_profile` and keep the complete detail within a 1400px maximum width. Do not put company copy, CSS, or internal notes into `pro_fields` or SEO fields, or treat the profile as product-specific configuration or lead-time promises.

Each fixed image block still contains only its heading and original image. Keep exactly six FAQs after the profile and all three image blocks. Inserting the text-only company profile does not require regenerating or reuploading images. The validator checks the complete profile, its single occurrence, and its position; missing or rewritten copy cannot pass.

Follow the user's supplied visual style: white background, compact hierarchy, and orange subsection headings. Keep five strengths in numbered order with the existing emphasis bolded. Align shipping, payment, and contact fields on desktop and allow natural wrapping on mobile. Do not add SVGs, icons, decorative card grids, dark panels, giant numbers, or large decorative areas. Bold emphasis and aligned labels are allowed; preserve the wording.

Use bold, centered H2 headings for Company Profile and its shipping, payment, and contact sections. Use the full available body width rather than narrowing the whole profile to half the screen. Strengths, mission, and markets each span the full width. Shipping and payment are independent side-by-side columns, as are address and contact information. Body text and inline labels are left-aligned; short content flows naturally on one line. Stack columns on narrow screens. The complete detail has a 1400px maximum width.

Keep outer left/right profile padding at zero on desktop and mobile, with vertical spacing only. Do not split a paragraph into two columns; field names and values remain together in their paragraph. Independent shipping and payment sections may sit beside one another without splitting their text.
