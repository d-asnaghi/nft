import json
import argparse
from pathlib import Path
import rocks


def json_config(name, description, address, png):
    return json.dumps({
        "name": f"{name}",
        "symbol": "",
        "description": f"{description}",
        "image": f"{png}",
        "seller_fee_basis_points": 0,
        "collection": {
            "name": "Rocks X NFT",
            "family": "Rocks"
        },
        "properties": {
            "files": [
                {
                    "uri": f"{png}",
                    "type": "image/png"
                }
            ],
            "creators": [
                {
                    "address": f"{address}",
                    "share": 100
                }
            ]
        }
    }, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=Path, help="output dir")
    args = parser.parse_args()

    for n in range(0, 5):

        config_path = args.dir / f"{n}.json"
        image_path = args.dir / f"{n}.png"

        attributes = rocks.attributes()
        image, metadata = rocks.rock(attributes)

        description = f"""{metadata["color"]} {metadata["style"]} Rock. Grown with love and affection"""

        with open(config_path, "w") as cfg:
            cfg.write(json_config(
                name=f"Test Friendly Rock #{n}",
                description=description,
                address="2Wbf3ZCrXzsKCRPSfbAmJ7gddEubwMqkhvBD7jeb9DmY",
                png=image_path.stem
            ))

        image.save(image_path)
