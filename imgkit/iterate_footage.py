import html
import json
import logging
import os
import shutil
import sqlite3
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

from imgkit.iter import iter_media
from imgkit.rename_stamp import stamp_owner_image, stamp_owner_video


def ingest_new_photos(
    input_dir: Path,
    prepared_dir: Path,
    database_path: Path,
    owner: str,
    extensions: set[str],
) -> int:
    """Copy and stamp unregistered photos; the database survives output deletion."""
    input_dir = Path(input_dir).expanduser().resolve()
    prepared_dir = Path(prepared_dir).expanduser().resolve()
    database_path = Path(database_path).expanduser().resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(input_dir)

    prepared_dir.mkdir(parents=True, exist_ok=True)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    processed = 0

    with sqlite3.connect(database_path) as database:
        database.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_photos (
                source_path TEXT PRIMARY KEY,
                source_size INTEGER NOT NULL,
                source_mtime_ns INTEGER NOT NULL,
                output_name TEXT NOT NULL UNIQUE
            )
            """
        )

        for source in iter_media(input_dir, extensions, recursive=True):
            relative_path = source.relative_to(input_dir).as_posix()
            try:
                source_stat = source.stat()
                previous = database.execute(
                    """
                    SELECT source_size, source_mtime_ns
                    FROM processed_photos WHERE source_path = ?
                    """,
                    (relative_path,),
                ).fetchone()
                if previous is not None:
                    if previous == (source_stat.st_size, source_stat.st_mtime_ns):
                        logging.info("SKIP %s (already registered)", relative_path)
                    else:
                        logging.error(
                            "Source changed after it was registered; leaving it "
                            "untouched: %s",
                            relative_path,
                        )
                    continue

                output_name = f"{owner}.{source.name}"
                collision = database.execute(
                    "SELECT source_path FROM processed_photos WHERE output_name = ?",
                    (output_name,),
                ).fetchone()
                if collision is not None:
                    raise FileExistsError(
                        f"{source} and {collision[0]} would both produce "
                        f"{output_name}"
                    )

                destination = prepared_dir / output_name
                if destination.exists():
                    raise FileExistsError(
                        f"Unregistered output already exists; refusing to overwrite: "
                        f"{destination}"
                    )

                temporary = destination.with_name(
                    f".{destination.stem}.tmp{destination.suffix}"
                )
                try:
                    shutil.copy2(source, temporary)
                    if source.suffix.lower() in {".jpg", ".jpeg"}:
                        stamp_owner_image(temporary, owner)
                    os.utime(
                        temporary,
                        ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns),
                    )
                    temporary.replace(destination)
                    try:
                        database.execute(
                            """
                            INSERT INTO processed_photos
                                (source_path, source_size, source_mtime_ns, output_name)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                relative_path,
                                source_stat.st_size,
                                source_stat.st_mtime_ns,
                                output_name,
                            ),
                        )
                        database.commit()
                    except Exception:
                        database.rollback()
                        destination.unlink(missing_ok=True)
                        raise
                finally:
                    temporary.unlink(missing_ok=True)

                logging.info("OK %s -> %s", relative_path, destination.name)
                processed += 1
            except Exception:
                logging.exception("FAIL %s", relative_path)

    return processed

def ingest_new_videos(
    input_dir: Path,
    prepared_dir: Path,
    database_path: Path,
    owner: str,
    extensions: set[str],
) -> int:
    """Copy and stamp unregistered videos; the database survives output deletion."""
    input_dir = Path(input_dir).expanduser().resolve()
    prepared_dir = Path(prepared_dir).expanduser().resolve()
    database_path = Path(database_path).expanduser().resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(input_dir)

    prepared_dir.mkdir(parents=True, exist_ok=True)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    processed = 0

    with sqlite3.connect(database_path) as database:
        database.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_videos (
                source_path TEXT PRIMARY KEY,
                source_size INTEGER NOT NULL,
                source_mtime_ns INTEGER NOT NULL,
                output_name TEXT NOT NULL UNIQUE
            )
            """
        )

        for source in iter_media(input_dir, extensions, recursive=True):
            relative_path = source.relative_to(input_dir).as_posix()
            try:
                source_stat = source.stat()
                previous = database.execute(
                    """
                    SELECT source_size, source_mtime_ns
                    FROM processed_videos WHERE source_path = ?
                    """,
                    (relative_path,),
                ).fetchone()
                if previous is not None:
                    if previous == (source_stat.st_size, source_stat.st_mtime_ns):
                        logging.info("SKIP %s (already registered)", relative_path)
                    else:
                        logging.error(
                            "Source changed after it was registered; leaving it "
                            "untouched: %s",
                            relative_path,
                        )
                    continue

                output_name = f"{owner}.{source.name}"
                collision = database.execute(
                    "SELECT source_path FROM processed_videos WHERE output_name = ?",
                    (output_name,),
                ).fetchone()
                if collision is not None:
                    raise FileExistsError(
                        f"{source} and {collision[0]} would both produce "
                        f"{output_name}"
                    )

                destination = prepared_dir / output_name
                if destination.exists():
                    raise FileExistsError(
                        f"Unregistered output already exists; refusing to overwrite: "
                        f"{destination}"
                    )

                temporary = destination.with_name(
                    f".{destination.stem}.tmp{destination.suffix}"
                )
                try:
                    shutil.copy2(source, temporary)
                    if source.suffix.lower() in {".mp4"}:
                        stamp_owner_video(temporary, owner)
                    os.utime(
                        temporary,
                        ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns),
                    )
                    temporary.replace(destination)
                    try:
                        database.execute(
                            """
                            INSERT INTO processed_videos
                                (source_path, source_size, source_mtime_ns, output_name)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                relative_path,
                                source_stat.st_size,
                                source_stat.st_mtime_ns,
                                output_name,
                            ),
                        )
                        database.commit()
                    except Exception:
                        database.rollback()
                        destination.unlink(missing_ok=True)
                        raise
                finally:
                    temporary.unlink(missing_ok=True)

                logging.info("OK %s -> %s", relative_path, destination.name)
                processed += 1
            except Exception:
                logging.exception("FAIL %s", relative_path)

    return processed


def _web_format(source_suffix: str) -> tuple[str, str]:
    suffix = source_suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return suffix, "JPEG"
    if suffix == ".png":
        return suffix, "PNG"
    if suffix == ".webp":
        return suffix, "WEBP"
    return ".jpg", "JPEG"


def _web_ready(image: Image.Image, image_format: str) -> Image.Image:
    if image_format in {"JPEG"}:
        return image.convert("RGB")
    if image_format in {"PNG", "WEBP"} and (
        image.mode in {"RGBA", "LA"} or "transparency" in image.info
    ):
        return image.convert("RGBA")
    return image.convert("RGB")


def _save_web_image(
    image: Image.Image,
    destination: Path,
    image_format: str,
    icc_profile: bytes | None,
    jpeg_quality: int,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(
        f".{destination.stem}.tmp{destination.suffix}"
    )
    options: dict[str, object] = {}
    if image_format == "JPEG":
        options.update(quality=jpeg_quality, optimize=True, progressive=True)
    elif image_format == "PNG":
        options["optimize"] = True
    elif image_format == "WEBP":
        options.update(quality=jpeg_quality, method=4)
    if icc_profile:
        options["icc_profile"] = icc_profile

    try:
        image.save(temporary, format=image_format, **options)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def _fit_dimensions(
    image: Image.Image, maximum: tuple[int, int]
) -> Image.Image:
    return ImageOps.contain(
        image, maximum, method=Image.Resampling.LANCZOS
    )


def _html_image_tag(
    source_path: str,
    caption: str,
    width: int,
    height: int,
) -> str:
    escaped_source = html.escape(source_path, quote=True)
    escaped_caption = html.escape(caption, quote=True)
    return (
        f'<img src="{escaped_source}" alt="{escaped_caption}" '
        f'width="{width}" height="{height}" class="imghplg-image" '
        f'title="{escaped_caption}" '
        'style="float: left; margin: 0 1em 1em 0;" />'
    )


def create_web_assets(
    prepared_dir: Path,
    web_dir: Path,
    html_output: Path,
    public_image_path: str,
    extensions: set[str],
    medium_max_size: tuple[int, int],
    large_max_size: tuple[int, int],
    thumbnail_size: tuple[int, int],
    jpeg_quality: int,
) -> list[Path]:
    """Build web variants and a Joomla HTML fragment from the curated folder."""
    prepared_dir = prepared_dir.expanduser().resolve()
    web_dir = web_dir.expanduser().resolve()
    html_output = html_output.expanduser().resolve()
    if not prepared_dir.is_dir():
        raise NotADirectoryError(prepared_dir)

    public_image_path = public_image_path.strip("/")
    if public_image_path and (
        Path(public_image_path).is_absolute()
        or ".." in Path(public_image_path).parts
    ):
        raise ValueError("Public image path must be relative to the Joomla root")
    public_image_path = (
        f"{public_image_path}/" if public_image_path else ""
    )

    web_dir.mkdir(parents=True, exist_ok=True)
    image_tags: list[str] = []
    generated: list[Path] = []

    for source in iter_images(prepared_dir, extensions, recursive=True):
        try:
            with Image.open(source) as opened:
                opened.load()
                original = ImageOps.exif_transpose(opened)
                icc_profile = opened.info.get("icc_profile")
                output_suffix, image_format = _web_format(source.suffix)
                ready = _web_ready(original, image_format)

                medium = _fit_dimensions(ready, medium_max_size)
                large = _fit_dimensions(ready, large_max_size)
                thumbnail = ImageOps.fit(
                    ready,
                    thumbnail_size,
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )

                stem = source.stem
                large_path = web_dir / f"{stem}{output_suffix}"
                medium_path = web_dir / f"{stem}-m{output_suffix}"
                thumbnail_path = web_dir / f"{stem}-t{output_suffix}"

                _save_web_image(
                    large, large_path, image_format, icc_profile, jpeg_quality
                )
                _save_web_image(
                    medium, medium_path, image_format, icc_profile, jpeg_quality
                )
                _save_web_image(
                    thumbnail,
                    thumbnail_path,
                    image_format,
                    icc_profile,
                    jpeg_quality,
                )

            public_medium_path = quote(
                f"{public_image_path}{medium_path.name}", safe="/-._~"
            )
            caption = f"EDIT CAPTION: {source.stem}"
            image_tags.append(
                _html_image_tag(
                    public_medium_path,
                    caption,
                    medium.width,
                    medium.height,
                )
            )
            generated.extend((large_path, medium_path, thumbnail_path))
            logging.info("WEB %s -> %s", source.name, medium_path.name)
        except Exception:
            logging.exception("WEB conversion failed for %s", source)

    html_output.parent.mkdir(parents=True, exist_ok=True)
    html_temporary = html_output.with_name(f".{html_output.name}.tmp")
    manifest_path = web_dir / ".hiking-assets.json"
    manifest_temporary = web_dir / ".hiking-assets.json.tmp"
    try:
        html_temporary.write_text(
            "\n\n".join(image_tags) + ("\n" if image_tags else ""),
            encoding="utf-8",
        )
        html_temporary.replace(html_output)
        manifest_temporary.write_text(
            json.dumps(
                [path.name for path in generated],
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        manifest_temporary.replace(manifest_path)
    finally:
        html_temporary.unlink(missing_ok=True)
        manifest_temporary.unlink(missing_ok=True)

    logging.info("Wrote Joomla fragment to %s", html_output)
    return generated
