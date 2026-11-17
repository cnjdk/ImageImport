from pathlib import Path

# Edit these paths before using the scripts. Two sets of directories for two very distinct use cases.
def default_input_dir(usage) -> Path:
    match usage:
        case "x":
            return Path("~/dryfish/X/Tmp").expanduser()
        case _:
           return Path("~/dryfish/photo/Tmp").expanduser()

def default_output_dir(usage) -> Path:
    match usage:
        case "x":
            return Path("~/dryfish/X/Untagged").expanduser()
        case _:
           return Path("~/dryfish/photo/Input").expanduser()


def default_owner(usage) -> str | None:
    match usage:
        case "x":
            return None
        case _:
           return "cnj.dk"
 
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif", ".webp"
}
VIDEO_EXTENSIONS  = {
    ".mp4", ".mpg",
}
