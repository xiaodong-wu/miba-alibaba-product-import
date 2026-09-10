"""Append the three supplied title/image blocks after generated detail HTML."""
import argparse
import json
from html import escape
from pathlib import Path

FIXED = [('Factory Photo', 'factory-photo.webp'), ('MiBA Logo Options', 'miba-logo-options.webp'), ('MiBA Accessory Options', 'miba-accessory-options.webp')]


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


def compose(detail, records, uploaded):
    if not detail.strip() or 'xb_import_v2' not in detail:
        raise ValueError('detail must be a nonempty namespaced HTML fragment')
    if 'miba_fixed_blocks' in detail:
        raise ValueError('detail already contains fixed blocks')
    return detail + fixed_suffix(records, uploaded)


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
    print('OK: three ordered title/image blocks appended')


if __name__ == '__main__':
    main()
