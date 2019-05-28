from io import BytesIO
from typing import Tuple, Optional, Union, BinaryIO

import exifread


def get_exif_data(file: Union[BytesIO, BinaryIO]) -> dict:
    return exifread.process_file(file)


def get_location(exif_data: dict) -> Optional[Tuple[float, float]]:

    lat = None
    lon = None

    gps_latitude = exif_data.get('GPS GPSLatitude')
    gps_latitude_ref = exif_data.get('GPS GPSLatitudeRef')
    gps_longitude = exif_data.get('GPS GPSLongitude')
    gps_longitude_ref = exif_data.get('GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = convert_to_degrees(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = convert_to_degrees(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon


def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

#
# with open('test.jpg', 'rb') as f:
#     my_data = get_exif_data(f)
# my_location = get_location(my_data)
# print(my_location)
