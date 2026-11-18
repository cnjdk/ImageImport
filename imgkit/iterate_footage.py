import logging
import shutil
from pathlib import Path

from PIL import Image, ImageOps

from imgkit.iter import iter_media
from imgkit.rename_stamp import stamp_owner_image, stamp_owner_video
from imgkit.transform import transformWebPToGif



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
        relative_path = source.relative_to(input_dir).as_posix()

        match source.suffix.lower():
            case ".webp":
                if owner:
                    output_name = f"{owner}.{source.stem}.gif"
                else:
                    output_name = f"{source.stem}.gif"
            case _:
                if owner:
                    output_name = f"{owner}.{source.name}"
                else:
                    output_name = f"{source.name}"
 
        destination = output_dir / output_name
        if destination.exists():
            raise FileExistsError(
                f"Unregistered output already exists; refusing to overwrite: "
                f"{destination}"
            )

        temporary = destination.with_name(
            f".{destination.stem}.tmp{destination.suffix}"
        )
        match source.suffix.lower():
            case ".webp":
                transformWebPToGif(source, temporary)
            case _:            
                shutil.copy2(source, temporary)

        match source.suffix.lower():
            case ".jpg" | ".jpeg":
                stamp_owner_image(temporary, owner)
            case _:
                pass

        temporary.replace(destination)
        temporary.unlink(missing_ok=True)
        logging.info("OK %s -> %s", relative_path, destination.name)
        source.unlink(missing_ok=True)
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
        match source.suffix.lower():
            case ".mp4" | ".mpg"    :
                stamp_owner_video(temporary, owner)
            case _:
                pass
        temporary.replace(destination)
        temporary.unlink(missing_ok=True)
 
        logging.info("OK %s -> %s", relative_path, destination.name)
        processed += 1

    return processed
