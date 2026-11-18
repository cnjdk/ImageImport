# Transform certain image formats
from PIL import Image, ImageOps
import shutil


def checkAnimatedWebP(source) -> bool:
    """Check if a WebP image is animated."""
    with Image.open(source) as im:
        try:
            return getattr(im, "is_animated", False)
        except AttributeError:
            return False

def transformWebPToGif(source, destination):
    """Transform a WebP image to a GIF image if it is animated, otherwise just copy the file."""
 
    with Image.open(source) as im:
        try:
            if getattr(im, "is_animated"): 
                im.save(destination, format="GIF",append_images=[im.seek(i) or im.copy() for i in range(1, im.n_frames)],optimize=True, loop=0)
                return True
        except AttributeError:
            pass
        shutil.copy2(source, destination)
    return True 
