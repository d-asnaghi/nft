
from PIL import Image
import random
from pathlib import Path
import os

TRAITS_DIR = Path("traits")


def trait_name(path: Path) -> str:
    return path.stem.removeprefix(path.parent.stem).replace("_", " ").strip()


def traits() -> dict:
    traits = {}

    categories = [Path(d) for d in os.scandir(TRAITS_DIR) if d.is_dir()]
    for category in categories:
        images = category.glob('*.png')
        traits[category.stem] = [(trait_name(img), img) for img in images]

    return traits


def nft(traits: dict, base_trait: str):
    metadata = []

    # Create base trait
    base_name, path = random.choice(traits[base_trait])
    metadata.append({"trait-type": base_trait,
                    "value": base_name})
    image = Image.open(path)

    # Add traits
    for trait, values in traits.items():
        if trait != base_trait:
            name, path = random.choice(values)
            metadata.append(
                {"trait-type": trait, "value": name})
            layer = Image.open(path)
            image.paste(layer, (0, 0), mask=layer)

    return image, metadata


def rock(attrs: dict):
    return nft(attrs, base_trait="material")


if __name__ == "__main__":

    traits = traits()
    for n in range(0, 3):
        image, attributes = rock(traits)
        print(attributes)
        image.show()
