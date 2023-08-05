from PIL import Image
import os


def slice_image(image_path: str) -> None:
    im = Image.open(image_path)
    im.close()
    upper, bottom = 0, 1020
    for i in range(0, (im.size[1] // 1020)):
        im = Image.open(image_path)
        im = im.crop((0, upper, im.size[0], bottom))
        im.save(f"{os.path.dirname(image_path)}/{i}.png")
        upper += 1020
        bottom += 1020
    os.remove(image_path)
