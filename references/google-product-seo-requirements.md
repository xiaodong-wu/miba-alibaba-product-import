# Google Search product optimization requirements

> English translation of the user-supplied requirements snapshot.
> Original scope: English product pages for the BNS Railings website.
> Version date: 2026-08-27.
> Objective: Help Google crawl, understand, and index product pages while improving search-result click-through, page experience, and inquiry conversion.

The BNS Railings brand, railing products, and specifications below are examples from the original document. Preserve their role as examples; do not transfer their identity or facts to MiBA products. This document is a supplied editorial specification, not an automatically updated official Google policy library.

## 1. Core principles

1. Meet real buyers' search and decision-making needs before arranging keywords.
2. Give every product page independent, accurate, verifiable content. Do not directly copy Alibaba or other websites.
3. Titles, body text, images, specifications, and structured data must describe the same product. Do not exaggerate or include information that is not visible on the page.
4. Use keywords naturally. Do not stuff keywords, hide text, or mass-produce low-value near-duplicate pages.
5. Google does not guarantee indexing or a particular ranking. Monitor and improve published pages through Search Console.

## 2. Keyword planning before publication

Define a clear set of search intents for each product page:

| Type | Purpose | Example |
| --- | --- | --- |
| Core product term | Identify the product category | stainless steel rod railing |
| Long-tail keyword | Describe material, structure, and use | stainless steel rod railing for balcony |
| Customization term | Address project and OEM needs | custom railing system, OEM railing |
| Application term | Match buying scenarios | stair railing, deck railing, hotel balcony railing |
| Manufacturer term | Describe supply capabilities | manufacturer, factory, supplier |
| Brand term | Establish brand recognition | BNS Railings |

Requirements:

- Select one primary keyword and two to five related long-tail terms per page.
- Do not duplicate pages for similar products by changing only a few keywords.
- Consider terminology used by both professional buyers and ordinary users.
- Do not add `meta keywords`; Google Search does not use that tag.

## 3. Product names and SEO metadata

### 3.1 Product title: page H1

Suggested structure:

`Customization term + Design/Material + Core Product Term + Main Application`

Add descriptive or manufacturer terms when useful, keeping the result natural, accurate, and readable. Use one main H1 per page.

Example:

`Custom Stainless Steel Rod Railing for Stairs and Balconies`

Avoid:

- Repeatedly stacking `manufacturer / supplier / factory / wholesale`.
- Packing every specification, application, and synonym into one title.
- Including materials, certifications, prices, or applications that do not match the actual product.

### 3.2 SEO title: HTML `<title>`

Suggested structure:

`Modifier + Long-Tail Keyword + Manufacturer Term | Brand`

Editorial requirements:

- Approximately 50–65 English characters, with an internal target near 60. This is an editorial standard for display and management, not a mandatory Google length.
- Use natural English Title Case, treating articles and prepositions according to normal English conventions.
- Give every page a unique title that accurately summarizes its product.
- Place the primary keyword near the beginning and the brand generally at the end.
- Avoid repeated all-caps wording, exclamation marks, or promotional language intended only to attract clicks.

Example:

`Durable Stainless Steel Rod Railing Manufacturer | BNS`

### 3.3 Meta description

Suggested structure:

`Brand + Product/Material + Core Benefit + Main Application + Customization Capability`

Editorial requirements:

- No more than 140 English characters. This is the project's internal editorial standard, not a fixed Google truncation rule.
- Use one or two natural sentences, unique to each page.
- Include real selling points such as 304/316 stainless steel, CAD design, OEM support, ease of installation, or project customization when supported.
- Do not state prices, lead times, certifications, or warranties that the page body does not explain.
- Google may generate a snippet from page text according to the query, so the first screen should also communicate product value clearly.

Example:

`BNS Railings supplies custom 304/316 stainless steel rod railing systems for stairs, balconies and decks, with CAD design and OEM support.`

## 4. URLs, site structure, and indexing

- Use short, readable English URL words that match the product, for example `custom-stainless-steel-rod-railing`.
- Use lowercase letters and hyphens. Avoid meaningless identifiers, complex parameters, and keyword stuffing.
- Maintain one preferred URL per product with a self-referencing `rel="canonical"`.
- Redirect duplicate or old URLs to the preferred page with HTTP 301; use canonical where redirection is not possible.
- Make product pages discoverable through category pages, related products, and breadcrumbs; do not create orphan pages.
- Include valid product URLs in an XML Sitemap and submit it through Google Search Console.
- Ensure product pages, CSS, JavaScript, and important images are not blocked by `robots.txt`, `noindex`, login, or access restrictions.
- Use separate URLs and correct `hreflang` for multilingual pages. Do not let automatically translated versions overwrite one another.

## 5. Product images

### 5.1 File standards

| Image type | Dimensions | File-size target | Format | Requirement |
| --- | --- | --- | --- | --- |
| Product thumbnails/gallery | 800 × 800px | No more than 100 KB each | WebP | Clear, complete product on a clean background |
| Detail illustrations | Actual layout dimensions | Approximately 100 KB each | WebP | Readable text and details |
| Application scenes | Recommended width of at least 1200px | Compress while retaining clarity | WebP | Plausible product structure and installation logic |

If 100 KB causes obvious degradation, prioritize buyers' ability to see details, then compress reasonably.

### 5.2 SEO and page implementation

- Use descriptive English filenames, for example `custom-stainless-steel-rod-railing-white-background.webp`.
- Give each important image concise, accurate, distinct alt text describing its content and relationship to the page.
- Do not stuff alt text with keywords, manufacturer terms, or unrelated applications.
- Place images near relevant headings and text. Explain the setting and product advantages beside application images.
- Do not lazy-load the primary image visible on the first screen. Images below the fold may be lazy-loaded.
- Serve responsive images appropriate to screen width rather than oversized desktop assets on phones.
- Image URLs must be directly accessible to Google and return normal status codes.
- Images must match the real product structure. AI-generated scenes must not contain incorrect posts, floating connections, or implausible installations.

## 6. Product-detail content structure

Recommended sequence:

1. **First-screen overview:** H1, product gallery, one value paragraph, and primary CTA.
2. **Product introduction:** materials, structure, finish, design features, and suitable projects.
3. **Specification table:** model, material, dimensions, thickness, finish, installation method, and customizable options.
4. **Product advantages:** factual explanations of corrosion resistance, durability, installation, maintenance, and customization capabilities where supported.
5. **Applications:** stairs, balconies, decks, hotels, commercial buildings, residential properties, or outdoor projects as relevant to the product.
6. **Project examples:** actual or reasonable illustrative installation outcomes with descriptions of the setting.
7. **Packaging and delivery:** packing method, protective measures, optional trade terms, and lead-time information.
8. **Certifications:** only genuine, valid certifications relevant to the product or factory.
9. **Factory/team/office scenes:** production, quality control, design, and service capabilities.
10. **Company and product advantages:** actual BNS Railings capabilities in the original domain example, avoiding empty slogans.
11. **FAQ:** approximately six valuable questions about materials, dimensions, installation, customization, samples, and lead times.

Content requirements:

- Write natural, professional, grammatical English.
- Divide long content into clear sections, paragraphs, lists, and tables.
- Write each page independently and update it when needed.
- Specifications, certifications, cases, and reviews must be verifiable; fabrication is prohibited.
- There is no minimum or maximum word count. Answer buyers' questions completely.
- Present important information as crawlable text, not only inside images.

## 7. Page experience and technical performance

- Support phones, tablets, and desktop screens.
- Use HTTPS and avoid mixed content, broken resources, and repeated redirects.
- Compress images, CSS, and JavaScript; reduce third-party scripts that block the first screen.
- Prevent noticeable layout shifts as important images and text load.
- Core Web Vitals targets, evaluated at the 75th percentile of real-user data:
  - LCP ≤ 2.5 seconds.
  - INP ≤ 200 milliseconds.
  - CLS ≤ 0.1.
- Monitor with PageSpeed Insights and the Search Console Core Web Vitals report.
- Ensure Google can render the main content and functions with JavaScript enabled. Do not show Googlebot a different page from the one users see.

## 8. Publication acceptance checklist

### Content and keywords

- [ ] The H1 is accurate, natural, and unique.
- [ ] The primary keyword matches the page's product.
- [ ] Body copy is independently written without keyword stuffing.
- [ ] Specifications, certifications, cases, reviews, and delivery information are verifiable.
- [ ] The FAQ answers six meaningful purchasing questions.

### SEO metadata

- [ ] The SEO title is unique and approximately 65 English characters, within the 50–65 editorial range above.
- [ ] The meta description is unique and no more than 140 English characters.
- [ ] The URL is short and readable.
- [ ] The page is not blocked by robots.txt, `noindex`, or login restrictions.

### Images and video

- [ ] Gallery images are 800 × 800px WebP, targeting no more than 100 KB each.
- [ ] Detail images are compressed toward 100 KB while remaining clear.
- [ ] Filenames and alt text accurately describe the content.
- [ ] The first-screen main image is not lazy-loaded; other images use lazy loading where appropriate.

## 9. Practices explicitly excluded

- Do not use `meta keywords` as an optimization tactic.
- Do not stuff synonymous keywords, location terms, manufacturer terms, or brands.
- Do not treat body length as a ranking target.
- Do not create large numbers of highly similar product pages to capture keywords.
- Do not copy complete Alibaba, competitor, or older product-page descriptions.
- Do not buy or mass-produce low-quality backlinks.
- Do not fabricate prices, stock, ratings, reviews, certifications, or project cases.
- Do not promise guaranteed indexing, first-page placement, or rankings within a fixed time.

## 10. Official reference

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
