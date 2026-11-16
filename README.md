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
(QuickTime) tags to MP4 files. Other supported formats are copied unchanged.
Originals in `INPUT_DIR` are never modified. The SQLite database registers each
successful import by its relative input path and file stat.

Already registered inputs are skipped even when their prepared copy has been
deleted. 

