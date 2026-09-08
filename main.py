import json
import sys
from pathlib import Path

from PIL import Image

import custom_utils

JSON_Date_Format = "%Y-%m-%d"
Photo_Date_Format = "%Y:%m:%d"
Photo_Time_Format = "%H:%M:%S"

target_dir = Path("Photos")

rename_log = {}
sorted_names = {}
errors = {}


def main():
    # ----- Import JSON file ----- #
    with open("Parameters/schedule.json", "r") as file:
        Trips = json.load(file)

    # ----- Sort Images based on their DateTime ----- #
    for item in Path("Photos").iterdir():
        # ----- Only handle .JPG files ----- #
        if item.suffix != ".JPG":
            errors[item.name] = "Not a JPG file!"
            continue

        # ----- Open image's EXIF data to extract DateTime ----- #
        Photo_datetime, EXIF_exists = custom_utils.extract_datetime(Image.open(item))

        # ----- Skip over images that don't have EXIF data ----- #
        if EXIF_exists == False:
            errors[item.name] = "Doesn't have EXIF info!"
            continue

        # ----- Find matching location from Trips JSON ----- #
        matched_location = custom_utils.find_matching_location(Photo_datetime, Trips)

        # ----- Check for collision >> Name Suggestion ----- # // Requires: sorted_names, target_dir, matched_location, Photo_datetime
        rename_log[item] = custom_utils.decide_name(
            sorted_names, target_dir, matched_location, Photo_datetime, item
        )

    # ----- Check if user is fine with renaming ----- #
    for original, target in rename_log.items():
        print(f"{original.name} >> {target.name}")

    # ----- Report Errors ----- #
    print("\n# ----- Errors ----- #")
    for name, error in errors.items():
        print(f"{name} >> {error}")

    ans = input("\nCan I Proceed?(y/n)")
    if ans != "y":
        sys.exit()

    # ----- Actually move the files ----- #
    for item, target in rename_log.items():
        item.rename(target)


if __name__ == "__main__":
    main()
