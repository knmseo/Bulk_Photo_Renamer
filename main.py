import json
from pathlib import Path

from PIL import Image

import custom_utils

JSON_Date_Format = "%Y-%m-%d"
Photo_Date_Format = "%Y:%m:%d"
Photo_Time_Format = "%H:%M:%S"

rename_log = {}


def main():
    # Import JSON file
    with open("Parameters/schedule.json", "r") as file:
        Trips = json.load(file)

    # Open images iteratively
    for item in Path("Photos").iterdir():
        if item.suffix != ".JPG":
            continue
        Photo_datetime, EXIF_exists = custom_utils.extract_datetime(Image.open(item))
        if EXIF_exists == False:
            continue
            print(f"No EXIF in {item}")
        matched_location = custom_utils.find_matching_location(Photo_datetime, Trips)
        print(f"{item} >>> {matched_location}")


if __name__ == "__main__":
    main()
