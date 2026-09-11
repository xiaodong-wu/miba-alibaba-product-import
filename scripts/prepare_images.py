"""Prepare role-aware WebP images from reviewed source assets; never generates images."""
import argparse
import hashlib
from compose_content import FIXED
import io
import json
import re
import tempfile
from pathlib import Path
from PIL import Image, ImageOps


def prepare(plan_path: Path, output: Path, min_quality: int = 70):
    plan = json.loads(plan_path.read_text(encoding='utf-8-sig'))
    items = plan.get('images', [])
    if not items:
        raise ValueError('image plan is empty')
    names = set()
    sources = []
    for item in items:
        name, role = item['name'], item['role']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in names:
            raise ValueError('image names must be unique descriptive kebab-case stems')
        names.add(name)
        if role not in {'cover', 'gallery', 'detail', 'scenario', 'supplied_static'}:
            raise ValueError('unknown image role')
        if role in {'cover', 'gallery', 'detail', 'scenario'} and item.get('generated') is not True:
            raise ValueError('cover/gallery/detail/scenario images must be recorded as newly generated')
        source = (plan_path.parent / item['source']).resolve()
        if not source.is_file():
            raise ValueError('an image source is missing')
        if role == 'supplied_static':
            expected = dict((file[:-5], title) for title, file in FIXED)
            if name not in expected or source.stem != expected[name]:
                raise ValueError('fixed image filename does not match its required title')
        sources.append(source)
    manifest_path = output.parent / (output.name + '.image-manifest.json')
    if output.exists() or manifest_path.exists():
        raise ValueError('output or manifest already exists; use a fresh directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with tempfile.TemporaryDirectory(dir=output.parent, prefix='.image-stage-') as temp:
        stage = Path(temp)
        for item, source in zip(items, sources):
            with Image.open(source) as original:
                if getattr(original, 'n_frames', 1) > 1:
                    raise ValueError('multiframe source requires explicit still selection')
                oriented = ImageOps.exif_transpose(original)
                alpha = oriented.mode in {'RGBA', 'LA'} or 'transparency' in oriented.info
                im = oriented.convert('RGBA' if alpha else 'RGB')
            role = item['role']
            if role in {'cover', 'gallery'}:
                im = ImageOps.pad(im, (800, 800), method=Image.Resampling.LANCZOS,
                                  color=(0, 0, 0, 0) if alpha else 'white')
            elif role != 'supplied_static':
                width = int(item.get('width', im.width))
                if width < 1 or (role == 'scenario' and width < 1200):
                    raise ValueError('invalid width; scenario must be at least 1200 px')
                if width > im.width:
                    raise ValueError('source too narrow; regenerate at the target resolution')
                im = im.resize((width, max(1, round(im.height * width / im.width))), Image.Resampling.LANCZOS)
            quality = 82
            while True:
                buf = io.BytesIO()
                im.save(buf, 'WEBP', quality=quality, method=6, alpha_quality=100)
                data = buf.getvalue()
                if role in {'scenario', 'supplied_static'} or len(data) <= 100_000 or quality <= min_quality:
                    break
                quality = max(min_quality, quality - 3)
            filename = item['name'] + '.webp'
            (stage / filename).write_bytes(data)
            records.append({'file': filename, 'role': role,
                            'generated': item.get('generated') is True,
                            'title': source.stem if role == 'supplied_static' else None,
                            'source_file': source.name,
                            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                            'width': im.width, 'height': im.height, 'bytes': len(data),
                            'quality': quality,
                            'size_review_required': role != 'scenario' and len(data) > 100_000})
        output.mkdir()
        for file in stage.iterdir():
            file.replace(output / file.name)
    manifest_path.write_text(json.dumps({'images': records}, indent=2), encoding='utf-8')
    return records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan', type=Path)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--min-quality', type=int, default=70)
    args = p.parse_args()
    if not 70 <= args.min_quality <= 82:
        p.error('--min-quality must be 70 through 82')
    try:
        records = prepare(args.plan, args.output_dir, args.min_quality)
    except (ValueError, OSError, KeyError) as exc:
        p.error(str(exc))
    print(f'OK: {len(records)} WebP images prepared; visually review all outputs')


if __name__ == '__main__':
    main()
