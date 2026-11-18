# Transform certain image formats

def transformWebPToGif(source, destination):
    """Transform a WebP image to a GIF image."""
    from PIL import Image, ImageOps

    with Image.open(source) as im:
        try:
            if getattr(im, "is_animated"): 
                print("image is animated")
        except AttributeError:
            pass
        im.save(destination, format="GIF",append_images=[im.seek(i) or im.copy() for i in range(1, im.n_frames)],optimize=True, loop=0)
 
