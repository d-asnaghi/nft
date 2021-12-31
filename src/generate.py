import json
import argparse
from pathlib import Path
import rocks


def json_config(name, description, attributes, address, png):
    return json.dumps({
        "name": f"{name}",
        "symbol": "",
        "description": f"{description}",
        "image": f"{png}",
        "seller_fee_basis_points": 10,
        "external_url": "https://asnaghi.me",
        "collection": {"name": "Rocks Collection", "family": "Rocks Family"},
        "attributes": attributes,
        "properties": {
            "files": [{"uri": f"{png}", "type": "image/png"}],
            "creators": [{"address": f"{address}", "share": 100}]
        }
    }, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=Path, help="output dir")
    parser.add_argument("--number", type=int, default=10,
                        help="number of images")
    args = parser.parse_args()

    # Cache the available traits
    traits = rocks.traits()

    for n in range(0, args.number):

        config_path = args.dir / f"{n}.json"
        image_path = args.dir / f"{n}.png"

        image, attributes = rocks.rock(traits)

        labels = {trait.lower(): value.lower() for trait, value in [
            (entry["trait-type"], entry['value']) for entry in attributes
        ]}

        description = f"A {labels['profession']} rock, made of {labels['material']}"

        with open(config_path, "w") as cfg:
            cfg.write(json_config(
                name=f"Rock #{n}",
                description=description,
                attributes=attributes,
                address="2Wbf3ZCrXzsKCRPSfbAmJ7gddEubwMqkhvBD7jeb9DmY",
                png=image_path.stem
            ))

        image.save(image_path)
