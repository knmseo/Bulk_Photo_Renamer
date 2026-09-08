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


def main():
    # ----- Import JSON file ----- #
    with open("Parameters/schedule.json", "r") as file:
        Trips = json.load(file)

    # ----- Sort Images based on their DateTime ----- #
    for item in Path("Photos").iterdir():
        # ----- Only handle .JPG files ----- #
        if item.suffix != ".JPG":
            continue

        # ----- Open image's EXIF data to extract DateTime ----- #
        Photo_datetime, EXIF_exists = custom_utils.extract_datetime(Image.open(item))

        # ----- Skip over images that don't have EXIF data ----- #
        if EXIF_exists == False:
            print(f"No EXIF in {item}")
            continue

        # ----- Find matching location from Trips JSON ----- #
        matched_location = custom_utils.find_matching_location(Photo_datetime, Trips)

        # ----- Check for collision >> Name Suggestion ----- #
        suggested_name = target_dir / Path(
            matched_location + " | " + str(Photo_datetime) + ".JPG"
        )

        # ----- Check for collision >> shift name until available ----- #
        if sorted_names.get(suggested_name, 0) == 0:
            final_name = suggested_name
            sorted_names[suggested_name] = 1
        else:
            final_name = target_dir / Path(
                matched_location
                + str(sorted_names[suggested_name])
                + " | "
                + str(Photo_datetime)
                + ".JPG"
            )
            sorted_names[suggested_name] += 1

        rename_log[item] = final_name

    # ----- Check if user is fine with renaming ----- #
    print(rename_log)
    ans = input("Can I Proceed?(y/n)")
    if ans != "y":
        sys.exit()

    # ----- Actually move the files ----- #
    for item in Path("Photos").iterdir():
        if item.suffix == ".JPG":
            item.rename(rename_log[item])


if __name__ == "__main__":
    main()
