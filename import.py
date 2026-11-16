import logging

from config import (
    INPUT_DIR,
    OUTPUT_DIR,
    OWNER,
)

from imgkit.iterate_footage import ingest_new_photos, ingest_new_videos


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    InputDir = input(f"Input directory [{INPUT_DIR}]: ") or INPUT_DIR
    OutputDir = input(f"Output directory [{OUTPUT_DIR}]: ") or OUTPUT_DIR
    Owner = input(f"Owner or artist [{OWNER}]: ") or OWNER
    IMAGE_EXTENSIONS = { ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff" }
    processed = ingest_new_photos(
        InputDir,
        OutputDir,
        Owner,
        IMAGE_EXTENSIONS
    )
    logging.info("Imported %d new photo(s)", processed)

    VIDEO_EXTENSIONS  = { ".mp4", ".mpg"}

    processed_videos = ingest_new_videos(
        InputDir,
        OutputDir,
        Owner,
        VIDEO_EXTENSIONS,
    )
    logging.info("Imported %d new video(s)", processed_videos)



if __name__ == "__main__":
    main()
