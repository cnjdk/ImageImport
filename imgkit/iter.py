from pathlib import Path
from typing import Iterator

# Adjust to whatever you actually process
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}

def iter_media (directory: str | Path,
                extensions: set[str] = IMAGE_EXTENSIONS,
                recursive: bool = False,
                sort: bool = True) -> Iterator[Path]:
    """
    Yield media file paths from a directory.

    - Filters by extension (case-insensitive).
    - Skips directories and non-files.
    - Sorts for deterministic processing order.
    - Optionally recurses into subdirectories.
    """
    root = Path(directory).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)

    pattern = "**/*" if recursive else "*"
    paths = (p for p in root.glob(pattern) if p.is_file()
             and p.suffix.lower() in extensions)

    if sort:
        # Sort by full path so ordering is stable and predictable
        paths = iter(sorted(paths))

    yield from paths


#Test
if __name__ == "__main__":
    from pathlib import Path
    for p in iter_images(Path(".")):
        print(p)