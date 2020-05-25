from models.vehicle_position import VehiclePositionModel
from data_processing.realtime_information import GTFSRealtime
from models.stop_times import StopTimesModel
from models.stops import StopsModel
import geopy.distance
import datetime
import pickle5 as pickle
import numpy as np
from scipy import stats


class AnalyzeSchedule:
    @staticmethod
    def analyze(year=2020, month=5, day=24, prefix="1"):
        model = VehiclePositionModel()
        stop_times = StopTimesModel().read_all()
        filtered = [x for x in stop_times if x.departure_time.startswith(prefix)]
        all_positions = model.read_all()
        all_positions_filtered = [x for x in all_positions if x.timestamp.year == year]
        res = []
        for x in filtered:
            stop_id = x.stop_id
            departure_time = x.departure_time
            stop = StopsModel().get_stop_by_id(stop_id)
            stop_lat = stop.stop_lat
            stop_lon = stop.stop_lon
            departure_time_datetime = datetime.datetime.strptime(departure_time, '%H:%M:%S')
            departure_time_datetime = departure_time_datetime.replace(year=year, month=month, day=day)
            departure_time_datetime = departure_time_datetime - datetime.timedelta(hours=3)
            date_from = departure_time_datetime - datetime.timedelta(minutes=3)
            date_to = departure_time_datetime + datetime.timedelta(minutes=3)
            trip_id = x.trip_id
            last_pos = None
            for y in all_positions_filtered:
                if y.trip_id == trip_id:
                    if date_from <= y.timestamp < date_to:
                        if last_pos is None:
                            last_pos = y
                        elif abs(departure_time_datetime - y.timestamp) < abs(departure_time_datetime - last_pos.timestamp):
                            last_pos = y
            if last_pos is not None:
                distance = geopy.distance.vincenty((stop_lat, stop_lon), (last_pos.latitude, last_pos.longitude)).m
                res.append((last_pos, distance))
        return res

    @staticmethod
    def __generate_time_periods(start_time, stop_time, time_delta_min: int):
        time_delta = datetime.timedelta(minutes=time_delta_min)
        time_periods = []
        current_time_start = start_time
        current_time_stop = start_time + time_delta
        while current_time_stop < stop_time:
            time_periods.append((current_time_start, current_time_stop))
            current_time_start = current_time_stop
            current_time_stop += time_delta
        return time_periods

    @staticmethod
    def calculate_average_miss(start_time, stop_time, time_delta_min: int):
        time_periods_repr = []
        time_periods = AnalyzeSchedule.__generate_time_periods(start_time, stop_time, time_delta_min)
        average_miss = []
        file = open("data.obj", 'rb')
        miss_obj = pickle.load(file)
        file.close()
        for start, stop in time_periods:
            curr_miss = []
            for miss in miss_obj:
                if start <= miss[0].timestamp < stop:
                    curr_miss.append(miss[1])
            time_delta_to_localize = datetime.timedelta(hours=3, minutes=time_delta_min // 2)
            time_periods_repr.append((start + time_delta_to_localize).strftime("%H:%M"))
            if len(curr_miss) > 0:
                mode = stats.mode(np.array(curr_miss))
                average_miss.append(mode[0][0])
            else:
                average_miss.append(0)
        return time_periods_repr, average_miss

    @staticmethod
    def calculate_percentage_schedule_hit(start_time, stop_time, time_delta_min: int):
        time_periods_repr, average_miss = AnalyzeSchedule.calculate_average_miss(start_time, stop_time, time_delta_min)
        percentage_hit = []
        for miss in average_miss:
            percentage_hit.append(((1 - (miss / 300)) * 100) if miss <= 300 else 0)
        return time_periods_repr, percentage_hit

    @staticmethod
    def get_all_miss():
        file = open("data.obj", 'rb')
        object_file = pickle.load(file)
        file.close()
        return [x[1] for x in object_file]

    @staticmethod
    def count_vehicle_per_time(start_time, stop_time, time_delta_min: int):
        time_periods_repr = []
        time_periods = AnalyzeSchedule.__generate_time_periods(start_time, stop_time, time_delta_min)
        count_vehicles = []
        model = VehiclePositionModel()
        for start, stop in time_periods:
            data = model.get_all_between_time(start, stop)
            distinct_data = GTFSRealtime.get_distinct_by_keys(data, ['vehicle_id'], lambda x, y: True)
            count_vehicles.append(len(distinct_data))
            time_delta_to_localize = datetime.timedelta(hours=3, minutes=time_delta_min // 2)
            time_periods_repr.append((start + time_delta_to_localize).strftime("%H:%M"))
        return time_periods_repr, count_vehicles
