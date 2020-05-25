from models import Model


class StopTimesModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS stop_times (" \
                             "trip_id        text," \
                             "departure_time text," \
                             "stop_id        bigint," \
                             "stop_sequence  bigint," \
                             "timepoint      bigint," \
                             "PRIMARY KEY (trip_id, stop_sequence))"
        insert_query = "INSERT INTO stop_times (trip_id, departure_time, stop_id, stop_sequence, timepoint) " \
                       "VALUES (%(trip_id)s, %(departure_time)s, %(stop_id)s, %(stop_sequence)s, %(timepoint)s) " \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM stop_times"
        count_all_query = "SELECT COUNT(*) FROM stop_times"
        fields = ["trip_id", "departure_time", "stop_id", "stop_sequence", "timepoint"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, StopTime)
        super()._get_session().execute("CREATE CUSTOM INDEX IF NOT EXISTS departure_time_prefix "
                                       "ON stop_times (departure_time) "
                                       "USING 'org.apache.cassandra.index.sasi.SASIIndex'")


    def get_all_with_time_prefix(self, time_prefix):
        select_query = "SELECT * FROM stop_times WHERE departure_time LIKE %(time_prefix)s"
        try:
            res = super()._get_session().execute(select_query, {"time_prefix": time_prefix})
        except Exception as e:
            print(e)
            return False
        return [super()._convert_row_to_obj(row) for row in res.all()]

    def get_by_trip_id(self, trip_id: str):
        select_query = "SELECT * FROM stop_times WHERE trip_id = %(trip_is)s"
        try:
            res = super()._get_session().execute(select_query, {"trip_id": trip_id})
        except Exception as e:
            print(e)
            return False
        return [super()._convert_row_to_obj(row) for row in res.all()]


class StopTime:
    def __init__(self, obj=None):
        if obj is not None:
            self.trip_id = obj["trip_id"]
            self.departure_time = obj["departure_time"]
            self.stop_id = obj["stop_id"]
            self.stop_sequence = obj["stop_sequence"]
            self.timepoint = obj["timepoint"]
