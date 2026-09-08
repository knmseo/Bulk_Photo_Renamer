from datetime import datetime
from pathlib import Path

from PIL import ExifTags

JSON_Date_Format = "%Y-%m-%d"
Photo_DateTime_Format = "%Y:%m:%d %H:%M:%S"
Photo_Time_Format = "%H:%M:%S"


def extract_datetime(img):
    exif_data = img.getexif()
    if exif_data:
        exif_ifd = exif_data.get_ifd(ExifTags.IFD.Exif)
        date_time_original = exif_ifd.get(ExifTags.Base.DateTimeOriginal)
        datetime_object = datetime.strptime(  # noqa: DTZ007
            date_time_original, Photo_DateTime_Format
        )
        EXIF_exists = True
    else:
        datetime_object = 0
        EXIF_exists = False

    return datetime_object, EXIF_exists


def extract_trip_data(trip):
    start_date = datetime.strptime(trip["start"], JSON_Date_Format)  # noqa: DTZ007
    end_date = datetime.strptime(  # noqa: DTZ007
        trip["end"] + " 23:59:59", JSON_Date_Format + " %H:%M:%S"
    )
    return start_date, end_date


def find_matching_location(Photo_DateTime, Trips):
    for trip in Trips:
        start, end = extract_trip_data(trip)
        if start <= Photo_DateTime <= end:
            matched_location = f"{trip['country']} - {trip['city']}"
            return matched_location
    matched_location = "Unknown"
    return matched_location


def shift_name(
    target_dir, matching_location, sorted_names, suggested_name, Photo_DateTime
):
    final_name = target_dir / Path(
        matching_location
        + "_"
        + str(sorted_names[suggested_name])
        + " | "
        + Photo_DateTime.strftime("%Y_%m_%d -  %Hh %Mm %Ss")
        + ".JPG"
    )
    return final_name


def decide_name(sorted_names, target_dir, matched_location, Photo_datetime, item):
    suggested_name = target_dir / Path(
        matched_location
        + " | "
        + Photo_datetime.strftime("%Y_%m_%d -  %Hh %Mm %Ss")
        + ".JPG"
    )

    # ----- Check for collision >> shift name until available ----- #
    if sorted_names.get(suggested_name, 0) == 0:
        final_name = suggested_name
        sorted_names[suggested_name] = 1
    else:
        final_name = shift_name(
            target_dir,
            matched_location,
            sorted_names,
            suggested_name,
            Photo_datetime,
        )
        sorted_names[suggested_name] += 1

    while final_name.exists() and item != final_name:
        final_name = shift_name(
            target_dir,
            matched_location,
            sorted_names,
            suggested_name,
            Photo_datetime,
        )
        sorted_names[suggested_name] += 1
    return final_name
