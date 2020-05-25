from models import Model


class RoutesModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS routes (" \
                             "route_id         bigint," \
                             "agency_id        bigint," \
                             "route_short_name text  ," \
                             "route_long_name  text  ," \
                             "route_type       int   ," \
                             "route_color      text  ," \
                             "PRIMARY KEY (route_id))"
        insert_query = "INSERT INTO routes (route_id, agency_id, route_short_name, route_long_name, " \
                       "route_type, route_color) " \
                       "VALUES (%(route_id)s, %(agency_id)s, %(route_short_name)s, %(route_long_name)s, " \
                       "%(route_type)s, %(route_color)s)" \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM routes"
        count_all_query = "SELECT COUNT(*) FROM routes"
        fields = ["route_id", "agency_id", "route_short_name", "route_long_name",
                  "route_type", "route_color"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, Route)

    def get_route_by_id(self, route_id):
        select_query = "SELECT * FROM routes WHERE route_id = %(route_id)s"
        try:
            res = super()._get_session().execute(select_query, {"route_id": route_id})
        except Exception as e:
            print(e)
            return False
        return super(RoutesModel, self)._convert_row_to_obj(res.one())


class Route:
    def __init__(self, obj=None):
        if obj is not None:
            self.route_id = obj["route_id"]
            self.agency_id = obj["agency_id"]
            self.route_short_name = obj["route_short_name"]
            self.route_long_name = obj["route_long_name"]
            self.route_type = obj["route_type"]
            self.route_color = obj["route_color"]
