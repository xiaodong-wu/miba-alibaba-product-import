"""Compose product detail, fixed company profile, three supplied image blocks, then the final FAQ section."""
import argparse
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path

FIXED = [('Factory Photo', 'factory-photo.webp'), ('MiBA Logo Options', 'miba-logo-options.webp'), ('MiBA Accessory Options', 'miba-accessory-options.webp')]
FRAME_OPEN = '<div class="miba_product_detail" style="width:100%;max-width:1400px;margin:0 auto;box-sizing:border-box;">'
FRAME_CLOSE = '</div>'
LAYOUT_STYLE = '''<style>
.miba_product_detail .xb_import_v2,.miba_product_detail section,.miba_product_detail .miba_fixed_blocks{padding-left:0!important;padding-right:0!important;box-sizing:border-box}
.miba_product_detail section{padding-top:28px;padding-bottom:28px}
.miba_product_detail h2{font-weight:700!important;text-align:center!important;margin:0 0 24px}
.miba_product_detail p{column-count:1!important}
@media(max-width:600px){.miba_product_detail section{padding-top:20px;padding-bottom:20px}}
</style>'''


def company_profile():
    """Return the user's fixed company copy and responsive layout verbatim."""
    return (Path(__file__).resolve().parent.parent / 'assets' / 'company-profile.html').read_text(encoding='utf-8')


def fixed_suffix(records, uploaded):
    if uploaded.get('complete') is not True:
        raise ValueError('all uploads must complete before composition')
    by_file = {r['file']: r for r in records}
    urls = {r['file']: r['direct_url'] for r in uploaded['uploaded']}
    blocks = []
    for title, filename in FIXED:
        r = by_file[filename]
        if r.get('role') != 'supplied_static' or r.get('title') != title:
            raise ValueError('fixed block image/title provenance mismatch')
        width, height = int(r['width']), int(r['height'])
        if width < 1 or height < 1:
            raise ValueError('invalid image dimensions')
        blocks.append(f'<section class="miba_fixed_block"><h2>{escape(title)}</h2>'
                      f'<img src="{escape(urls[filename], quote=True)}" alt="{escape(title)}" '
                      f'width="{width}" height="{height}" loading="lazy" '
                      'style="display:block;width:100%;height:auto;"></section>')
    return '\n<div class="xb_import_v2 miba_fixed_blocks">' + ''.join(blocks) + '</div>'


def split_faq(fragment):
    """Extract one marked FAQ section without reserializing the authored HTML."""
    class FAQParser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.offsets = [0]
            for line in fragment.splitlines(keepends=True):
                self.offsets.append(self.offsets[-1] + len(line))
            self.start = self.end = None
            self.depth = self.count = 0

        def absolute_offset(self):
            line, col = self.getpos()
            return self.offsets[line - 1] + col

        def handle_starttag(self, tag, attrs):
            if 'miba_faq_section' in (dict(attrs).get('class') or '').split():
                self.count += 1
                if tag != 'section' or self.count != 1:
                    raise ValueError('FAQ must be one section marked miba_faq_section')
                self.start = self.absolute_offset()
                self.depth = 1
            elif self.depth and tag == 'section':
                self.depth += 1

        def handle_endtag(self, tag):
            if self.depth and tag == 'section':
                self.depth -= 1
                if not self.depth:
                    self.end = fragment.index('>', self.absolute_offset()) + 1

    parser = FAQParser()
    parser.feed(fragment)
    if parser.count != 1 or parser.end is None:
        raise ValueError('detail requires one complete miba_faq_section at the end')
    after = fragment[parser.end:]
    if not re.fullmatch(r'\s*(?:</[a-zA-Z][\w:-]*>\s*)*', after):
        raise ValueError('FAQ must be the final content section')
    return fragment[:parser.start] + after, fragment[parser.start:parser.end]


def compose(detail, records, uploaded):
    if not detail.strip() or 'xb_import_v2' not in detail:
        raise ValueError('detail must be a nonempty namespaced HTML fragment')
    if any(marker in detail for marker in ('miba_fixed_blocks', 'miba_product_detail', 'miba_company_profile')):
        raise ValueError('detail already contains fixed blocks')
    body, faq = split_faq(detail)
    return FRAME_OPEN + body.rstrip() + company_profile() + fixed_suffix(records, uploaded) + LAYOUT_STYLE + faq + FRAME_CLOSE


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--detail-file', type=Path, required=True)
    p.add_argument('--image-manifest', type=Path, required=True)
    p.add_argument('--upload-manifest', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('output already exists; choose a fresh output path')
    result = compose(args.detail_file.read_text(encoding='utf-8'),
                     json.loads(args.image_manifest.read_text(encoding='utf-8'))['images'],
                     json.loads(args.upload_manifest.read_text(encoding='utf-8')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding='utf-8')
    print('OK: product detail, company profile, three ordered image blocks, then final FAQ composed')


if __name__ == '__main__':
    main()
