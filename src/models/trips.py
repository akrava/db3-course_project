from models import Model


class TripsModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS trips (" \
                             "route_id      bigint," \
                             "service_id    bigint," \
                             "trip_id       text  ," \
                             "direction_id  int  ," \
                             "trip_headsign text  ," \
                             "block_id      int  ," \
                             "shape_id      int  ," \
                             "PRIMARY KEY (trip_id))"
        insert_query = "INSERT INTO trips (route_id, service_id, trip_id, direction_id, " \
                       "trip_headsign, block_id, shape_id) " \
                       "VALUES (%(route_id)s, %(service_id)s, %(trip_id)s, %(direction_id)s, " \
                       "%(trip_headsign)s, %(block_id)s, %(shape_id)s) " \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM trips"
        count_all_query = "SELECT COUNT(*) FROM trips"
        fields = ["route_id", "service_id", "trip_id", "direction_id",
                  "trip_headsign", "block_id", "shape_id"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, Trip)


class Trip:
    def __init__(self, obj=None):
        if obj is not None:
            self.route_id = obj["route_id"]
            self.service_id = obj["service_id"]
            self.trip_id = obj["trip_id"]
            self.direction_id = obj["direction_id"]
            self.trip_headsign = obj["trip_headsign"]
            self.block_id = obj["block_id"]
            self.shape_id = int(obj["shape_id"])
