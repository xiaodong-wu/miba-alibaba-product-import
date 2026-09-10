"""Compare CSVs and validate detail with three fixed image blocks; no upload and no secret values in reports."""
import argparse
from compose_content import FIXED, fixed_suffix
import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image

GENERATED = {'title', 'remark', 'content', 'pro_fields', 'file_name', 'seo_title1',
             'seo_desc', 'thumb', 'scenario_image', 'images'}
REQUIRED = GENERATED | {'link', 'IMGBB_API_KEY'}
CHECKS = ('facts_verified', 'fixed_blocks_verified', 'original_detail_images_verified',
          'visual_review_passed', 'seo_document_reviewed')
CJK = re.compile(r'[\u3400-\u9fff\U00020000-\U0002fa1f]')
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')


class HTML(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.images, self.h1, self.faq, self.scripts = [], 0, 0, 0
        self.meta_keywords = False
        self.namespaced = False
        self.parts = []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.h1 += tag == 'h1'
        self.scripts += tag == 'script'
        classes = (a.get('class') or '').split()
        self.faq += bool({'pd_faq_item', 'xb_faq_item'} & set(classes))
        self.namespaced |= 'xb_import_v2' in classes
        self.meta_keywords |= tag == 'meta' and (a.get('name') or '').lower() == 'keywords'
        if tag == 'img':
            self.images.append(a)

    def handle_data(self, data):
        self.parts.append(data)


def direct(value):
    if not value or any(c.isspace() for c in value):
        return False
    try:
        u = urlsplit(value)
        return (u.scheme == 'https' and u.hostname == 'i.ibb.co' and
                not u.username and not u.password and u.port in (None, 443) and
                u.path.lower().endswith('.webp') and not u.fragment and not u.query)
    except ValueError:
        return False


def read_csv(path):
    csv.field_size_limit(sys.maxsize)
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def validate(source, output, images_dir, review):
    errors, warnings = [], []
    counts = {'success': 0, 'skipped': 0, 'blocked': 0, 'blank': 0}
    def err(n, message):
        errors.append({'row_number': n, 'message': message})
    in_headers, originals = read_csv(source)
    headers, rows = read_csv(output)
    if len(set(headers)) != len(headers) or len(set(in_headers)) != len(in_headers):
        err(None, 'duplicate CSV headers')
    if not REQUIRED.issubset(headers):
        err(None, 'missing required output columns')
    if not {'link', 'IMGBB_API_KEY'}.issubset(in_headers):
        err(None, 'missing required input columns')
    if headers[:len(in_headers)] != in_headers:
        err(None, 'original column order changed')
    if len(rows) != len(originals):
        err(None, 'row count changed')
    reviews = {}
    for item in review.get('rows', []):
        n = item.get('row_number')
        if n in reviews:
            err(n, 'duplicate review record')
        reviews[n] = item
    unique = {f: set() for f in ('file_name', 'seo_title1', 'seo_desc')}
    for n, (before, row) in enumerate(zip(originals, rows), 2):
        if None in before or None in row or any(v is None for v in row.values()):
            err(n, 'malformed CSV row')
            continue
        for field in in_headers:
            if field not in GENERATED and row.get(field) != before.get(field):
                err(n, 'a protected source field or unknown column changed')
        populated = any((before.get(f) or '').strip() for f in before if f != 'IMGBB_API_KEY')
        if not populated:
            counts['blank'] += 1
            if any((row.get(f) or '').strip() for f in GENERATED):
                err(n, 'blank source row acquired generated content')
            continue
        entry = reviews.get(n, {})
        status = entry.get('status')
        if status not in {'success', 'skipped', 'blocked'}:
            err(n, 'missing or invalid row review status')
            continue
        counts[status] += 1
        if status != 'success':
            if not entry.get('reason'):
                err(n, 'skipped/blocked row requires a reason in review file')
            for field in GENERATED:
                if (row.get(field) or '') != (before.get(field) or ''):
                    err(n, 'skipped/blocked row changed generated fields; keep drafts separately')
                    break
            continue
        if not all(entry.get('checks', {}).get(k) is True for k in CHECKS):
            err(n, 'manual review checklist is incomplete')
        if not entry.get('evidence'):
            err(n, 'evidence file reference is missing')
        try:
            u = urlsplit(row.get('link', ''))
            host = u.hostname or ''
            if u.scheme not in ('https', 'http') or not (host == 'alibaba.com' or host.endswith('.alibaba.com')):
                err(n, 'source is not an Alibaba URL')
        except ValueError:
            err(n, 'source URL is invalid')
        if not (row.get('IMGBB_API_KEY') or '').strip():
            err(n, 'row API key is empty')
        content = row.get('content') or ''
        prefix = content
        for f in GENERATED:
            value = prefix if f == 'content' else row.get(f, '')
            if not value.strip():
                err(n, f'{f} is empty')
            if CJK.search(value):
                err(n, f'{f} contains Chinese characters')
        if not 50 <= len(row.get('seo_title1', '')) <= 65:
            err(n, 'SEO title must be 50 to 65 characters under the supplied editorial standard')
        if len(row.get('seo_desc', '')) > 140:
            err(n, 'SEO description exceeds 140 characters')
        for f, values in unique.items():
            value = row.get(f, '').strip().casefold()
            if value in values:
                err(n, f'duplicate {f}')
            values.add(value)
        slug = row.get('file_name', '')
        if not SLUG.fullmatch(slug):
            err(n, 'file_name must be a lowercase kebab-case slug')
        lines = [line.strip() for line in row.get('pro_fields', '').splitlines() if line.strip()]
        if not 4 <= len(lines) <= 8 or any(re.match(r'^(?:[.•●▪◦‣⁃*+\-–—]|\d+[.)])', x) for x in lines):
            err(n, 'pro_fields must be 4 to 8 unbulleted plain lines')
        gallery = {}
        alts = set()
        for line in row.get('images', '').splitlines():
            url, sep, alt = line.partition('|')
            if not sep or not direct(url) or not alt.strip():
                err(n, 'invalid gallery URL/alt entry')
                continue
            if url in gallery or alt.strip().casefold() in alts:
                err(n, 'duplicate gallery URL or alt')
            gallery[url] = alt
            alts.add(alt.strip().casefold())
        for field in ('thumb', 'scenario_image'):
            url = row.get(field, '')
            if not direct(url) or url not in gallery:
                err(n, f'{field} must be a Direct WebP URL included in images')
        parsed, full = HTML(prefix), HTML(content)
        if not parsed.namespaced:
            err(n, 'prefix is missing xb_import_v2 wrapper')
        if parsed.scripts or parsed.meta_keywords:
            err(n, 'new fragment contains script or meta keywords')
        if full.h1 > 1:
            err(n, 'combined HTML contains multiple H1 elements')
        if full.h1 == 0:
            warnings.append({'row_number': n, 'message': 'verify the CMS supplies exactly one external H1'})
        if full.faq != 6:
            err(n, 'combined HTML must contain exactly six FAQ items using xb_faq_item or pd_faq_item')
        if not parsed.images:
            err(n, 'new detail must contain original application imagery')
        for img in parsed.images:
            if img.get('src') not in gallery or not img.get('alt', '').strip():
                err(n, 'new image must have a gallery Direct URL and nonempty alt')
            if not (img.get('width') or '').isdigit() or not (img.get('height') or '').isdigit():
                err(n, 'new image requires explicit numeric width and height')
        if parsed.images and parsed.images[0].get('loading') == 'lazy':
            err(n, 'first new image must not be lazy loaded')
        if row.get('scenario_image') not in {im.get('src') for im in parsed.images}:
            err(n, 'new detail must include the application image')
        if 'application concept visualization' not in ''.join(parsed.parts).lower():
            err(n, 'new detail must label the simulated application visualization')
        if SLUG.fullmatch(slug):
            folder = images_dir / slug
            manifest_path = images_dir / (slug + '.image-manifest.json')
            try:
                records = json.loads(manifest_path.read_text(encoding='utf-8'))['images']
                files = list(folder.iterdir())
                if not records or any(not f.is_file() or f.suffix.lower() != '.webp' for f in files):
                    err(n, 'final image folder must contain only WebP files')
                if len(files) != len(records) or {f.name for f in files} != {r['file'] for r in records}:
                    err(n, 'image manifest and actual files differ')
                if len(gallery) != len(records):
                    err(n, 'gallery and local image counts differ')
                if not any(r['role'] == 'scenario' for r in records):
                    err(n, 'missing local scenario image')
                upload_path = images_dir.parent / 'upload-manifests' / (slug + '.json')
                uploaded = json.loads(upload_path.read_text(encoding='utf-8'))
                if uploaded.get('complete') is not True:
                    err(n, 'upload manifest is incomplete')
                local_records = {r['file']: r for r in records}
                urls = {r['direct_url']: local_records.get(r['file']) for r in uploaded['uploaded']}
                if set(urls) != set(gallery) or any(v is None for v in urls.values()):
                    err(n, 'upload manifest, local images and CSV gallery do not match')
                tail = fixed_suffix(records, uploaded)
                if not content.endswith(tail):
                    err(n, 'content must end with the three exact title/image blocks in order')
                else:
                    detail = content[:-len(tail)]
                    if 'miba_fixed_block' in detail:
                        err(n, 'fixed blocks must occur only once at the end')
                    for img in HTML(detail).images:
                        local = urls.get(img.get('src'))
                        if not local or local.get('generated') is not True:
                            err(n, 'product detail uses an image without generated provenance')
                fixed_urls = {r['file']: r['direct_url'] for r in uploaded['uploaded']}
                expected_order = [fixed_urls[name] for _, name in FIXED]
                if list(gallery)[-3:] != expected_order:
                    err(n, 'gallery must end with the three fixed images in order')
                scenario = urls.get(row.get('scenario_image'))
                cover = urls.get(row.get('thumb'))
                if not scenario or scenario.get('role') != 'scenario':
                    err(n, 'scenario_image does not map to a local scenario image')
                if not cover or cover.get('role') != 'cover':
                    err(n, 'thumb does not map to a local cover image')
                for record in records:
                    name = record['file']
                    if Path(name).name != name:
                        err(n, 'invalid manifest filename')
                        continue
                    with Image.open(folder / name) as im:
                        im.load()
                        if im.format != 'WEBP':
                            err(n, 'image does not decode as WebP')
                        if record['role'] in {'cover', 'gallery'} and im.size != (800, 800):
                            err(n, 'cover/gallery must be 800 by 800')
                        if record['role'] == 'scenario' and im.width < 1200:
                            err(n, 'scenario width is below 1200')
                    if record['role'] in {'scenario', 'detail'} and record.get('generated') is not True:
                        err(n, 'detail/scenario lacks generated-image provenance')
                    if record['role'] != 'scenario' and (folder / name).stat().st_size > 100_000:
                        warnings.append({'row_number': n, 'message': 'image exceeds 100 KB; confirm readability exception in review notes'})
            except (OSError, ValueError, KeyError, TypeError):
                err(n, 'local images or image manifest cannot be validated')
    outcome = 'failed' if errors else 'partial' if counts['skipped'] or counts['blocked'] else 'passed'
    if not rows or not any(counts[k] for k in ('success', 'blocked', 'skipped')):
        err(None, 'CSV has no reviewed populated rows')
        outcome = 'failed'
    return {'result': outcome, 'counts': counts, 'errors': errors, 'warnings': warnings,
            'deployment_status': 'requires site-level verification; not certified by this script'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--images-dir', type=Path, required=True)
    p.add_argument('--review', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    args = p.parse_args()
    result = validate(args.source, args.output, args.images_dir,
                      json.loads(args.review.read_text(encoding='utf-8-sig')))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"{result['result']}: {len(result['errors'])} errors, {len(result['warnings'])} warnings")
    raise SystemExit({'passed': 0, 'failed': 1, 'partial': 2}[result['result']])


if __name__ == '__main__':
    main()
