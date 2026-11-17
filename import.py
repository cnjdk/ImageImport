from email import parser
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
    # parser = argparse.ArgumentParser(
    #     description="Ingest new photos and videos from a directory, stamping them with the owner's name."
    # )
    # parser.add_argument(
    #     "-i", "--input_dir",
    #     type=str,
    #     default="",
    #     help="Input directory to scan for new media files."
    # )
    # parser.add_argument(
    #     "-o", "--output_dir",
    #     type=str,
    #     default="",
    #     help="Output directory to copy and stamp media files."
    # )
    # parser.add_argument(
    #     "-u", "--owner",
    #     type=str,
    #     default="",
    #     help="Owner or artist name to stamp on media files."
    # )
    # parser.add_argument(
    #     "-x", "--xusage",
    #     type=str,
    #     default="",
    #     help="Specify for alternate set of defaults"
    # )
    # args = parser.parse_args()
    # inputDir = default_input_dir(args.xusage)
    # if args.input_dir:
    #     inputDir = Path(args.input_dir).expanduser().resolve()
    # else:
    #   inputDir = input(f"Input directory [{default_input_dir(args.xusage)}]: ") or default_input_dir(args.xusage)

    inputDir = input(f"Input directory [{default_input_dir('x')}]: ") or default_input_dir('x')

    # outputDir = default_output_dir(args.xusage)
    # if args.output_dir:
    #     outputDir = Path(args.output_dir).expanduser().resolve()
    # else:
    #    outputDir = input(f"Output directory [{default_output_dir(args.xusage)}]: ") or default_output_dir(args.xusage) 
    outputDir = input(f"Output directory [{default_output_dir('x')}]: ") or default_output_dir('x') 

    # owner = default_owner(args.xusage)
    # if args.owner:
    #     owner = args.owner
    # else:
    #     owner = input(f"Owner name [{default_owner(args.xusage)}]: ") or default_owner(args.xusage)
    owner = input(f"Owner name [{default_owner('x')}]: ") or default_owner('x')


    processed = ingest_new_photos(
        inputDir,
        outputDir,
        owner,
        IMAGE_EXTENSIONS
    )
    logging.info("Imported %d new photo(s)", processed)

    VIDEO_EXTENSIONS  = { ".mp4", ".mpg"}

    processed_videos = ingest_new_videos(
        inputDir,
        outputDir,
        owner,
        VIDEO_EXTENSIONS,
    )
    logging.info("Imported %d new video(s)", processed_videos)



if __name__ == "__main__":
    main()
