"""This snippet combines an image (histology.png) with its exported segmentation (segmentation.png) in a way that it
draws a 2-pixel wide red outline where segmentation changes, leaving everything else intact.

From Gargely Scucs (https://www.nitrc.org/forum/forum.php?thread_id=12684&forum_id=9082)
"""

import PIL.Image

overlay = PIL.Image.open("segmentation.png")
image = PIL.Image.open("histology.png")

for x in range(1, image.width - 1):
    for y in range(1, image.height - 1):
        x0 = x * overlay.width / image.width
        y0 = y * overlay.height / image.height
        p = overlay.getpixel((x0, y0))
        if (p != overlay.getpixel(((x - 1) * overlay.width / image.width, y0))
                or p != overlay.getpixel(((x + 1) * overlay.width / image.width, y0))
                or p != overlay.getpixel((x0, (y - 1) * overlay.height / image.height))
                or p != overlay.getpixel((x0, (y + 1) * overlay.height / image.height))):
            image.putpixel((x, y), (255, 0, 0))

image.save("outline.png", "PNG")
