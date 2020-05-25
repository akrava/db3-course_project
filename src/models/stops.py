from models import Model


class StopsModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS stops (" \
                             "stop_id   bigint," \
                             "stop_name text,  " \
                             "stop_desc text,  " \
                             "stop_lat  double," \
                             "stop_lon  double," \
                             "PRIMARY KEY (stop_id))"
        insert_query = "INSERT INTO stops (stop_id, stop_name, stop_desc, stop_lat, stop_lon) " \
                       "VALUES (%(stop_id)s, %(stop_name)s, %(stop_desc)s, %(stop_lat)s, %(stop_lon)s) " \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM stops"
        count_all_query = "SELECT COUNT(*) FROM stops"
        fields = ["stop_id", "stop_name", "stop_desc", "stop_lat", "stop_lon"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, Stop)

    def get_stop_by_id(self, stop_id):
        select_query = "SELECT * FROM stops WHERE stop_id = %(stop_id)s"
        try:
            res = super()._get_session().execute(select_query, {"stop_id": stop_id})
        except Exception as e:
            print(e)
            return False
        return super(StopsModel, self)._convert_row_to_obj(res.one())


class Stop:
    def __init__(self, obj=None):
        if obj is not None:
            self.stop_id = obj["stop_id"]
            self.stop_name = obj["stop_name"]
            self.stop_desc = obj["stop_desc"] if isinstance(obj["stop_desc"], str) else ""
            self.stop_lat = obj["stop_lat"]
            self.stop_lon = obj["stop_lon"]
