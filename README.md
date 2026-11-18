# Image processing

Part of GitHub project cnjdk/Image-Processing. Slightly altered. The sole purpose
is to prepare media for import into Digikam. The values below become default values
that can be overridden

## Configure

Edit the literal paths and settings near the top of config.py file
for the tablet:

- `INPUT_DIR`: incoming image files.
- `OUTPUT_DIR`: byte-preserving copies used for manual review.

Install dependencies with `python3 -m pip install -r requirements.txt`.

## 1. Import new footage

Run `python3 import.py` after copying new footage into `INPUT_DIR`. The script
recursively copies supported photos to `OUTPUT_DIR`, prepends owner info to
the filename, and adds Artist/Copyright EXIF tags to JPEG copies and iTunes-style
(QuickTime) tags to MP4 files. WEBP files are converted into GIF, probably animated.
Other supported formats are copied unchanged.
Originals in `INPUT_DIR` are deleted after modification. 

Supports two sets of defaults: If no parameters are specified, it will use my
standard photo workflow. If "-a x" is specified, it will use my special purpose
workflow. In both cases, it will prompt you whether you can accept the defaults and
you can override the choice. 

You can also specify the three values, input directory, output directory, owner/artist name
on the command line using -i, -o and -u respectively. In these case it will use the values
without prompt.


