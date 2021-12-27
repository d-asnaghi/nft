
from PIL import Image
import random
from pathlib import Path
import os


def base() -> Image.Image:
    image = Image.open("attributes/base.png")
    return image.convert('RGBA')


def attr_name(path: Path) -> str:
    return path.stem.removeprefix(path.parent.stem).replace("_", " ").strip().title()


def attributes() -> dict:
    path = Path("attributes")
    attributes = {}

    categories = [Path(d) for d in os.scandir(path) if d.is_dir()]
    for category in categories:
        images = category.glob('*.png')
        attributes[category.stem] = [(attr_name(img), img) for img in images]

    return attributes


def random_color():
    colors = ["red", "purple", "green", "yellow", "black"]
    return random.choice(colors)


def color_overlay(image: Image, color, mask: Image = None, alpha: float = 0.2) -> Image:
    image = Image.blend(image, Image.new('RGBA', image.size, color), alpha)

    if mask:
        r, g, b, _ = image.split()
        _, _, _, a = mask.split()
        return Image.merge('RGBA', (r, g, b, a))
    return image


def nft(base: Image.Image, attrs: dict):
    image = base
    metadata = {}

    # Add a color overlay
    metadata["color"] = random_color().title()
    image = color_overlay(image, metadata["color"], mask=image)

    # Paste attributes
    for attribute, values in attrs.items():
        name, path = random.choice(values)
        metadata[attribute] = name
        layer = Image.open(path)
        image.paste(layer, (0, 0), mask= layer)

    return image, metadata


def rock(attrs: dict):
    return nft(base(), attrs)


if __name__ == "__main__":

    attrs = attributes()
    for n in range(0, 3):
        image, metadata = rock(attrs)
        print(metadata)
        image.show()
