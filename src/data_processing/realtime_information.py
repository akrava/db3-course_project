from google.transit import gtfs_realtime_pb2
from models.vehicle_position import VehiclePosition, VehiclePositionModel
import requests


class GTFSRealtime:
    def __init__(self):
        self.__URL = "http://track.ua-gis.com/gtfs/lviv/vehicle_position"
        self.__feed = gtfs_realtime_pb2.FeedMessage()

    def get_bytes(self):
        return requests.get(self.__URL).content

    def parse(self, data: bytes):
        self.__feed.ParseFromString(data)
        return self.__feed.entity

    @staticmethod
    def __check_if_obj_has_fields(obj, fields: [str]):
        for field in fields:
            if not obj.HasField(field):
                return False
        return True

    @staticmethod
    def __filter_condition(feed):
        if not GTFSRealtime.__check_if_obj_has_fields(feed, ['id', 'vehicle']) \
                or (feed.HasField('is_deleted') and feed.is_deleted):
            return False
        vehicle = feed.vehicle
        if not GTFSRealtime.__check_if_obj_has_fields(vehicle, ['trip', 'position', 'timestamp', 'vehicle']):
            return False
        trip = vehicle.trip
        valid_schedule_relationship = gtfs_realtime_pb2.TripUpdate.StopTimeUpdate.ScheduleRelationship.SCHEDULED
        if not GTFSRealtime.__check_if_obj_has_fields(trip, ['trip_id', 'schedule_relationship', 'route_id']) \
                or trip.schedule_relationship != valid_schedule_relationship:
            return False
        position = vehicle.position
        if not GTFSRealtime.__check_if_obj_has_fields(position, ['latitude', 'longitude', 'bearing', 'odometer',
                                                                 'speed']):
            return False
        vehicle_id = vehicle.vehicle
        if not GTFSRealtime.__check_if_obj_has_fields(vehicle_id, ['id', 'license_plate']):
            return False
        return True

    @staticmethod
    def get_distinct_by_keys(values, keys, lambda_compare):
        data_dict = dict()
        for val in values:
            value_of_key = val
            for key in keys:
                value_of_key = getattr(value_of_key, key)
            if value_of_key not in data_dict or lambda_compare(val, data_dict[value_of_key]):
                data_dict[value_of_key] = val
        return list(data_dict.values())

    @staticmethod
    def __get_newest_feed(cur_feed, feed_to_compare):
        return cur_feed.vehicle.timestamp > feed_to_compare.vehicle.timestamp

    def filter_data(self, feed_entities: []):
        data = [feed for feed in feed_entities if self.__filter_condition(feed)]
        data = self.get_distinct_by_keys(data, ['id'], self.__get_newest_feed)
        return self.get_distinct_by_keys(data, ['vehicle', 'vehicle', 'id'], self.__get_newest_feed)

    def save_current_feed_to_db(self):
        data = self.get_bytes()
        entities = self.parse(data)
        filtered = self.filter_data(entities)
        objects_to_save = [VehiclePosition(x) for x in filtered]
        model = VehiclePositionModel()
        for obj in objects_to_save:
            model.create(obj)
