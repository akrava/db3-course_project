from models.agency import Agency, AgencyModel
from models.routes import Route, RoutesModel
from models.shapes import Shape, ShapesModel
from models.stop_times import StopTime, StopTimesModel
from models.stops import Stop, StopsModel
from models.trips import Trip, TripsModel
from data_processing.realtime_information import GTFSRealtime
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

    def save_static_info_to_db(self):
        self.save_zip()
        result = self.parse()

        agency = [Agency(x) for x in result["agency"].T.to_dict().values()]
        print("Uploading agency...")
        if not all([AgencyModel().create(x) for x in agency]):
            print("Error while uploading agency")

        routes = [Route(x) for x in result["routes"].T.to_dict().values()]
        print("Uploading routes...")
        if not all([RoutesModel().create(x) for x in routes]):
            print("Error while uploading routes")

        shapes = [Shape(x) for x in result["shapes"].T.to_dict().values()]
        shapes = GTFSRealtime.get_distinct_by_keys(shapes, ['shape_id'], lambda x, y: True)
        print("Uploading shapes...")
        if not all([ShapesModel().create(x) for x in shapes]):
            print("Error while uploading shapes")

        stop_times = [StopTime(x) for x in result["stop_times"].T.to_dict().values()]
        print("Uploading stop times...")
        if not all([StopTimesModel().create(x) for x in stop_times]):
            print("Error while uploading stop times")

        stops = [Stop(x) for x in result["stops"].T.to_dict().values()]
        print("Uploading stops...")
        if not all([StopsModel().create(x) for x in stops]):
            print("Error while uploading stops")

        trips = [Trip(x) for x in result["trips"].T.to_dict().values() if float(x["shape_id"]).is_integer()]
        print("Uploading trips...")
        if not all([TripsModel().create(x) for x in trips]):
            print("Error while uploading trips")
