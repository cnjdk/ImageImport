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
    input_dir:      Path,
    output_dir:     Path,
    owner:          str,
    extensions:     set[str],
) -> int:
    """Copy and stamp photos;"""
    input_dir = Path(input_dir).expanduser().resolve()
    output_dir= Path(output_dir).expanduser().resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(input_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    processed = 0

 
    for source in iter_media(input_dir, extensions, recursive=False):
        output_name = f"{owner}.{source.name}"

        destination = output_dir / output_name
        if destination.exists():
            raise FileExistsError(
                f"Unregistered output already exists; refusing to overwrite: "
                f"{destination}"
            )

        temporary = destination.with_name(
            f".{destination.stem}.tmp{destination.suffix}"
        )
        shutil.copy2(source, temporary)
        if source.suffix.lower() in {".jpg", ".jpeg"}:
            stamp_owner_image(temporary, owner)
        temporary.replace(destination)
        temporary.unlink(missing_ok=True)
        logging.info("OK %s -> %s", relative_path, destination.name)
        processed += 1
    return processed

def ingest_new_videos(
    input_dir:      Path,
    output_dir:   Path,
    owner:          str,
    extensions:     set[str],
    ) -> int:
     input_dir = Path(input_dir).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(input_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    processed = 0

    for source in iter_media(input_dir, extensions, recursive=False):
        relative_path = source.relative_to(input_dir).as_posix()
        output_name = f"{owner}.{source.name}"
 
        destination = output_dir / output_name
        if destination.exists():
            raise FileExistsError(
                f"Unregistered output already exists; refusing to overwrite: "
                f"{destination}"
            )

        temporary = destination.with_name(
            f".{destination.stem}.tmp{destination.suffix}"
        )
        shutil.copy2(source, temporary)
        if source.suffix.lower() in {".mp4"}:
            stamp_owner_video(temporary, owner)
        os.utime(
            temporary,
            ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns),
        )
        temporary.replace(destination)
        temporary.unlink(missing_ok=True)
 
        logging.info("OK %s -> %s", relative_path, destination.name)
        processed += 1

    return processed
