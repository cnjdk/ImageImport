from pathlib import Path

OWNER = "cnj.dk"

# Edit these paths for the tablet before using the scripts.
INPUT_DIR   = Path("C:/Users/antro/kDrive/Pictures/Camera Roll").expanduser()
OUTPUT_DIR  = Path("//dryfish.local/photo/Output").expanduser()

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif", ".webp"
}
VIDEO_EXTENSIONS  = {
    ".mp4", ".mpg",
}
