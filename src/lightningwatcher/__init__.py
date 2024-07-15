# imports
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from google.cloud import storage
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


def test():
    return True
