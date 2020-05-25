from models import Model
from datetime import datetime
from dateutil import tz
import pytz


class VehiclePositionModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS vehicle_position (" \
                             "id             bigint   ," \
                             "route_id       text     ," \
                             "trip_id        text     ," \
                             "latitude       double   ," \
                             "longitude      double   ," \
                             "speed          double   ," \
                             "bearing        double   ," \
                             "odometer       double   ," \
                             "timestamp      timestamp," \
                             "vehicle_id     text     ," \
                             "license_plate  text     ," \
                             "PRIMARY KEY ((id, trip_id), timestamp)) " \
                             "WITH CLUSTERING ORDER BY (timestamp DESC)"
        insert_query = "INSERT INTO vehicle_position (id, route_id, trip_id, latitude, longitude, speed, bearing, " \
                       "odometer, timestamp, vehicle_id, license_plate) " \
                       "VALUES (%(id)s, %(route_id)s, %(trip_id)s, %(latitude)s, %(longitude)s, %(speed)s, " \
                       "%(bearing)s, %(odometer)s, %(timestamp)s, %(vehicle_id)s, %(license_plate)s) " \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM vehicle_position"
        count_all_query = "SELECT COUNT(*) FROM vehicle_position"
        fields = ["id", "route_id", "trip_id", "latitude", "longitude", "speed", "bearing",
                  "odometer", "timestamp", "vehicle_id", "license_plate"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, VehiclePosition)

    def _convert_obj_to_params(self, obj):
        res = super()._convert_obj_to_params(obj)
        res["id"] = int(obj.id) + obj.timestamp
        res["timestamp"] = datetime.utcfromtimestamp(obj.timestamp)
        return res

    def _convert_row_to_obj(self, row):
        res = super()._convert_row_to_obj(row)
        # res.timestamp = res.timestamp.replace(tzinfo=pytz.timezone('Europe/Kiev')).astimezone(tz=None)
        return res

    def get_all_between_time(self, start_time, end_time):
        select_query = "SELECT * FROM vehicle_position WHERE timestamp >= %(start_time)s " \
                       "AND timestamp < %(end_time)s ALLOW FILTERING"
        try:
            res = super()._get_session().execute(select_query, {"start_time": start_time, "end_time": end_time})
        except Exception as e:
            print(e)
            return False
        return [self._convert_row_to_obj(row) for row in res.all()]

    def get_all_between_time_with_trip_id(self, start_time, end_time, trip_id):
        select_query = "SELECT * FROM vehicle_position WHERE trip_id = %(trip_id)s " \
                       " ALLOW FILTERING"
        #               "AND timestamp >= %(start_time)s AND timestamp < %(end_time)s ALLOW FILTERING"
        try:
            res = super()._get_session().execute(select_query, {
                "start_time": start_time,
                "end_time": end_time,
                "trip_id": trip_id
            })
        except Exception as e:
            print(e)
            return False
        return [self._convert_row_to_obj(row) for row in res.all()]

    def get_all_speeds(self):
        select_query = "SELECT speed FROM vehicle_position"
        try:
            res = super()._get_session().execute(select_query)
        except Exception as e:
            print(e)
            return False
        return [row.speed for row in res.all()]

    def get_all_route_ids(self):
        select_query = "SELECT route_id FROM vehicle_position"
        try:
            res = super()._get_session().execute(select_query)
        except Exception as e:
            print(e)
            return False
        return [row.route_id for row in res.all()]


class VehiclePosition:
    def __init__(self, feed_entity=None):
        if feed_entity is not None:
            self.id = feed_entity.id
            vehicle_obj = feed_entity.vehicle
            self.route_id = vehicle_obj.trip.route_id
            self.trip_id = vehicle_obj.trip.trip_id
            self.latitude = vehicle_obj.position.latitude
            self.longitude = vehicle_obj.position.longitude
            self.speed = vehicle_obj.position.speed
            self.bearing = vehicle_obj.position.bearing
            self.odometer = vehicle_obj.position.odometer
            self.timestamp = vehicle_obj.timestamp
            self.vehicle_id = vehicle_obj.vehicle.id
            self.license_plate = vehicle_obj.vehicle.license_plate
