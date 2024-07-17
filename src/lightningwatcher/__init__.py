# imports
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from google.cloud import storage
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset


def __download_gcloud_public_file__(bucket_id: str, remote_path: str, local_path: str):
    client = storage.Client.create_anonymous_client()
    bucket = client.get_bucket(bucket_id)
    blob = bucket.get_blob(remote_path)
    blob.download_to_filename(local_path)


def __list_blobs_with_prefix__(bucket_name: str, prefix: str):
    """
    Lists all the blobs in the bucket that begin with the prefix.
    Does not return any subdirectories.
    """
    client = storage.Client.create_anonymous_client()
    blobs = client.list_blobs(bucket_name, prefix=prefix, delimiter="/")

    return blobs


def __get_blobs_for_datetime__(
    dataset: str, satellite: str, date_of_interest: datetime
):
    prefix_path = f"{satellite}/{date_of_interest.year:04}/{date_of_interest.timetuple().tm_yday:03}/{date_of_interest.hour:02}/"
    return __list_blobs_with_prefix__(dataset, prefix_path)


DATASET = "gcp-public-data-goes-16"
SATELLITE = "GLM-L2-LCFA"
YEAR = 2024
MONTH = 7
DAY = 16
HOUR = 22
DATETIME = datetime(YEAR, MONTH, DAY, HOUR)
FILE = f"{YEAR}-{MONTH}-{DAY}-{HOUR}.nc"


def main():
    if not os.path.exists(FILE):
        blobs = list(__get_blobs_for_datetime__(DATASET, SATELLITE, DATETIME))
        blobs[0].download_to_filename(FILE)

    g16glm = Dataset(FILE, "r")

    event_lat = g16glm.variables["event_lat"][:]
    event_lon = g16glm.variables["event_lon"][:]

    group_lat = g16glm.variables["group_lat"][:]
    group_lon = g16glm.variables["group_lon"][:]

    flash_lat = g16glm.variables["flash_lat"][:]
    flash_lon = g16glm.variables["flash_lon"][:]

    fig = plt.figure(figsize=(6, 6), dpi=200)
    # map = Basemap(
    #     projection="tmerc",
    #     resolution="i",
    #     lat_0=42.5,
    #     lon_0=-75,
    #     llcrnrlat=40.0,
    #     llcrnrlon=-80.0,
    #     urcrnrlat=45.0,
    #     urcrnrlon=-70.0,
    # )

    map = Basemap(
        projection="aea",
        resolution="i",
        lat_0=42.5,
        lon_0=-75,
        lat_1=40.0,
        lat_2=45.0,
        llcrnrlat=40.0,
        llcrnrlon=-80.0,
        urcrnrlat=45.0,
        urcrnrlon=-70.0,
    )

    # map = Basemap(
    #     projection="merc",
    #     lat_0=41.38,
    #     lon_0=-73.57,
    #     resolution="f",
    #     llcrnrlat=41.30,
    #     llcrnrlon=-74.18,
    #     urcrnrlat=41.45,
    #     urcrnrlon=-74.00
    # )

    map.shadedrelief()
    # map.drawcoastlines()
    map.drawcountries()
    map.drawstates()
    # map.drawrivers()
    # map.drawmapboundary()

    # map.bluemarble()

    # Plot events as large blue dots
    # event_x, event_y = map(event_lon, event_lat)
    # map.plot(event_x, event_y, "bo", markersize=7)

    # Plot groups as medium green dots
    # group_x, group_y = map(group_lon, group_lat)
    # map.plot(group_x, group_y, "go", markersize=3)

    # Plot flashes as small red dots
    flash_x, flash_y = map(flash_lon, flash_lat)
    map.plot(flash_x, flash_y, "ro", markersize=1)

    plt.show()


def test():
    return True


if __name__ == "__main__":
    main()
