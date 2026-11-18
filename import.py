import logging
import argparse
from pathlib import Path

from config import (
    default_input_dir,
    default_output_dir,
    default_owner,
    IMAGE_EXTENSIONS,
    VIDEO_EXTENSIONS,
)

from imgkit.iterate_footage import ingest_new_photos, ingest_new_videos


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest new photos and videos from a directory, stamping them with the owner's name."
    )
    parser.add_argument(
        "-i", "--input_dir",
        type=str,
        default="",
        help="Input directory to scan for new media files."
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default="",
        help="Output directory to copy and stamp media files."
    )
    parser.add_argument(
        "-u", "--owner",
        type=str,
        default="",
        help="Owner or artist name to stamp on media files."
    )
    parser.add_argument(
        "-a", "--alternate_usage",
        type=str,
        default="",
        help="Specify for alternate set of defaults"
    )
    args = parser.parse_args()
    alt = None
    if args.alternate_usage:
        alt = args.alternate_usage
    
    
    inputDir = default_input_dir(alt)
    if args.input_dir:
        inputDir = Path(args.input_dir).expanduser().resolve()
    else:
      inputDir = input(f"Input directory [{default_input_dir(alt)}]: ") or default_input_dir(alt)

    outputDir = default_output_dir(alt)
    if args.output_dir:
        outputDir = Path(args.output_dir).expanduser().resolve()
    else:
       outputDir = input(f"Output directory [{default_output_dir(alt)}]: ") or default_output_dir(alt) 
 
    owner = default_owner(alt)
    if args.owner:
        owner = args.owner
    else:
        owner = input(f"Owner name [{default_owner(alt)}]: ") or default_owner(alt)
 

    processed = ingest_new_photos(
        inputDir,
        outputDir,
        owner,
        IMAGE_EXTENSIONS
    )
    logging.info("Imported %d new photo(s)", processed)

    processed_videos = ingest_new_videos(
        inputDir,
        outputDir,
        owner,
        VIDEO_EXTENSIONS,
    )
    logging.info("Imported %d new video(s)", processed_videos)



if __name__ == "__main__":
    main()
