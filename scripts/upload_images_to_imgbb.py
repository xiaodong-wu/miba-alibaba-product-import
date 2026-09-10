#!/usr/bin/env python3
"""Upload WebP product images to ImgBB and emit Direct-link metadata."""

from __future__ import annotations

import argparse
import csv
import json
import re
import secrets
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


API_URL = "https://api.imgbb.com/1/upload"
MAX_IMAGE_BYTES = 32_000_000
API_KEY_FIELD = "IMGBB_API_KEY"


def natural_key(path: Path) -> list[tuple[int, int | str]]:
    return [
        (0, int(part)) if part.isdigit() else (1, part.lower())
        for part in re.split(r"(\d+)", path.name)
    ]


def is_webp(path: Path) -> bool:
    try:
        signature = path.read_bytes()[:12]
    except OSError:
        return False
    return (
        len(signature) == 12
        and signature[:4] == b"RIFF"
        and signature[8:12] == b"WEBP"
    )


def collect_images(image_dir: Path) -> list[Path]:
    if not image_dir.is_dir():
        raise ValueError(f"image directory not found: {image_dir}")
    images = sorted(
        (
            path
            for path in image_dir.iterdir()
            if path.is_file() and path.suffix.lower() == ".webp"
        ),
        key=natural_key,
    )
    if not images:
        raise ValueError(f"no WebP images found in {image_dir}")
    for path in images:
        size = path.stat().st_size
        if size > MAX_IMAGE_BYTES:
            raise ValueError(
                f"{path.name} is {size:,} bytes; ImgBB maximum is "
                f"{MAX_IMAGE_BYTES:,} bytes"
            )
        if not is_webp(path):
            raise ValueError(f"{path.name} does not contain valid WebP data")
    return images


def read_api_key(csv_file: Path, row_number: int) -> str:
    csv.field_size_limit(sys.maxsize)
    if not csv_file.is_file():
        raise ValueError(f"CSV file not found: {csv_file}")
    if row_number < 2:
        raise ValueError("CSV row number must be 2 or greater")

    with csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        if API_KEY_FIELD not in headers:
            raise ValueError(f"CSV is missing required field {API_KEY_FIELD}")
        for current_row, row in enumerate(reader, start=2):
            if current_row != row_number:
                continue
            api_key = (row.get(API_KEY_FIELD) or "").strip()
            if not api_key:
                raise ValueError(
                    f"CSV row {row_number} has an empty {API_KEY_FIELD} field"
                )
            return api_key

    raise ValueError(f"CSV row {row_number} does not exist")


def multipart_body(api_key: str, image_path: Path) -> tuple[bytes, str]:
    boundary = f"----CodexImgBB{secrets.token_hex(16)}"
    safe_name = image_path.name.replace('"', "")
    chunks = [
        f"--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="key"\r\n\r\n',
        api_key.encode(),
        b"\r\n",
        f"--{boundary}\r\n".encode(),
        (
            f'Content-Disposition: form-data; name="name"\r\n\r\n'
            f"{image_path.stem}\r\n"
        ).encode(),
        f"--{boundary}\r\n".encode(),
        (
            f'Content-Disposition: form-data; name="image"; '
            f'filename="{safe_name}"\r\n'
        ).encode(),
        b"Content-Type: image/webp\r\n\r\n",
        image_path.read_bytes(),
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    return b"".join(chunks), boundary


def is_direct_webp_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return (
        parsed.scheme.lower() == "https"
        and (parsed.hostname or "").lower() == "i.ibb.co"
        and parsed.path.lower().endswith(".webp")
    )


def upload_once(
    image_path: Path,
    api_key: str,
    timeout: float,
) -> dict[str, object]:
    body, boundary = multipart_body(api_key, image_path)
    request = Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": "miba-alibaba-product-import/2.0",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        http_status = getattr(response, "status", 200)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("ImgBB returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("ImgBB returned an unexpected JSON value")

    if http_status != 200 or not payload.get("success"):
        status = payload.get("status", http_status)
        error_data = payload.get("error")
        error = (
            error_data.get("message", "upload failed")
            if isinstance(error_data, dict)
            else str(error_data or "upload failed")
        )
        raise RuntimeError(f"ImgBB status {status}: {error}")

    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("ImgBB response is missing its data object")
    direct_url = str(data.get("url") or "")
    if not is_direct_webp_url(direct_url):
        raise RuntimeError("ImgBB response is missing a WebP data.url Direct link")

    return {
        "file": image_path.name,
        "direct_url": direct_url,
        "width": data.get("width"),
        "height": data.get("height"),
        "size": data.get("size"),
    }


def upload_with_retries(
    image_path: Path,
    api_key: str,
    timeout: float,
    retries: int,
) -> dict[str, object]:
    for attempt in range(retries + 1):
        try:
            return upload_once(image_path, api_key, timeout)
        except HTTPError as exc:
            retriable = exc.code == 429 or 500 <= exc.code < 600
            error: Exception = RuntimeError(f"ImgBB HTTP {exc.code}")
        except (URLError, TimeoutError) as exc:
            retriable = True
            detail = exc.reason if isinstance(exc, URLError) else exc
            error = RuntimeError(f"ImgBB connection error: {detail}")
        except Exception:
            raise

        if not retriable or attempt == retries:
            raise error
        time.sleep(min(2**attempt, 8))

    raise RuntimeError("upload retry loop ended unexpectedly")


def write_manifest(path: Path, payload: dict[str, object], force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"manifest already exists: {path}; pass --force to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            mode="w",
            encoding="utf-8",
            delete=False,
        ) as temporary:
            json.dump(payload, temporary, indent=2, ensure_ascii=True)
            temporary.write("\n")
            temporary_path = Path(temporary.name)
        temporary_path.replace(path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image_dir", type=Path, help="Folder containing final WebP images")
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Optional JSON output path for public Direct-link metadata",
    )
    parser.add_argument(
        "--csv-file",
        type=Path,
        required=True,
        help=f"CSV containing the per-row {API_KEY_FIELD} field",
    )
    parser.add_argument(
        "--row-number",
        type=int,
        required=True,
        help="One-based CSV data-row number whose ImgBB key should be used",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60,
        help="Per-upload timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retry count for rate limits and transient failures (default: 2)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing manifest",
    )
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.retries < 0:
        parser.error("--retries must not be negative")
    if args.manifest and args.manifest.exists() and not args.force:
        parser.error(
            f"manifest already exists: {args.manifest}; pass --force to replace it"
        )
    try:
        api_key = read_api_key(args.csv_file, args.row_number)
        images = collect_images(args.image_dir)
    except ValueError as exc:
        parser.error(str(exc))

    uploaded: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    for image in images:
        print(f"Uploading {image.name}...", file=sys.stderr)
        try:
            uploaded.append(
                upload_with_retries(
                    image,
                    api_key,
                    args.timeout,
                    args.retries,
                )
            )
        except Exception as exc:
            errors.append({"file": image.name, "error": str(exc)})
            print(f"ERROR: {image.name}: {exc}", file=sys.stderr)

    payload: dict[str, object] = {
        "provider": "ImgBB",
        "complete": not errors and len(uploaded) == len(images),
        "uploaded": uploaded,
        "errors": errors,
    }
    if args.manifest:
        try:
            write_manifest(args.manifest, payload, args.force)
        except OSError as exc:
            print(f"ERROR: could not write manifest: {exc}", file=sys.stderr)
            return 1
        print(f"Manifest: {args.manifest}", file=sys.stderr)
    else:
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=True)
        sys.stdout.write("\n")

    if errors:
        print(
            f"FAILED: {len(errors)} of {len(images)} image(s) failed",
            file=sys.stderr,
        )
        return 1
    print(f"OK: uploaded {len(uploaded)} image(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
