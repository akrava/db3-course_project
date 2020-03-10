import requests
import zipfile
import shutil
import os
import pandas as pd


class GTFSStatic:
    def __init__(self):
        self.__URL = "http://track.ua-gis.com/gtfs/lviv/static.zip"
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.__temp_dir = os.path.join(cur_dir, '../../temp')
        self.__archive_name = "gtfs_static.zip"

    def save_zip(self):
        if os.path.exists(self.__temp_dir):
            shutil.rmtree(self.__temp_dir)
        os.mkdir(self.__temp_dir)
        data = requests.get(self.__URL).content
        with open(os.path.join(self.__temp_dir, self.__archive_name), "wb") as file:
            file.write(data)

    def __load_csv(self, file_name: str):
        return pd.read_csv(os.path.join(self.__temp_dir, file_name))

    def parse(self):
        with zipfile.ZipFile(os.path.join(self.__temp_dir, self.__archive_name), 'r') as zip_ref:
            zip_ref.extractall(self.__temp_dir)
        result = {
            "agency": self.__load_csv("agency.txt"),
            "routes": self.__load_csv("routes.txt"),
            "shapes": self.__load_csv("shapes.txt"),
            "stop_times": self.__load_csv("stop_times.txt"),
            "stops": self.__load_csv("stops.txt"),
            "trips": self.__load_csv("trips.txt")
        }
        shutil.rmtree(self.__temp_dir)
        return result
