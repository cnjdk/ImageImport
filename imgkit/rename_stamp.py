# imgkit/rename_stamp.py
import shutil
import logging
from pathlib import Path

import piexif

from mutagen.mp4 import MP4



def stamp_owner_image(path: Path, owner: str) -> None:
    """Insert Artist and Copyright EXIF tags into a JPEG, modifying it in place."""
    exif_dict = piexif.load(str(path))
    exif_dict["0th"][piexif.ImageIFD.Artist]    = owner.encode("utf-8")
    exif_dict["0th"][piexif.ImageIFD.Copyright] = f"© {owner}".encode("utf-8")
    piexif.insert(piexif.dump(exif_dict), str(path))


# Add iTunes-style (QuickTime) tags to videos using mutagen library
def stamp_owner_video(path: Path, owner: str) -> None:
    """Write Artist and Copyright tags into an MP4 file."""
    video = MP4(str(path))
    video["\xa9ART"] = [owner]              # ©ART — Artist
    video["cprt"]  = [f"© {owner}"]         # Copyright
    video.save()
