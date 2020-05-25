from models import Model


class ShapesModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS shapes (" \
                             "shape_id            bigint," \
                             "shape_pt_lat        double," \
                             "shape_pt_lon        double," \
                             "shape_pt_sequence   double," \
                             "shape_dist_traveled double,"\
                             "PRIMARY KEY (shape_id, shape_pt_sequence))"
        insert_query = "INSERT INTO shapes (shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, " \
                       "shape_dist_traveled) " \
                       "VALUES (%(shape_id)s, %(shape_pt_lat)s, %(shape_pt_lon)s, " \
                       "%(shape_pt_sequence)s, %(shape_dist_traveled)s)" \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM shapes"
        count_all_query = "SELECT COUNT(*) FROM shapes"
        fields = ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence",
                  "shape_dist_traveled"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, Shape)


class Shape:
    def __init__(self, obj=None):
        if obj is not None:
            self.shape_id = int(obj["shape_id"])
            self.shape_pt_lat = obj["shape_pt_lat"]
            self.shape_pt_lon = obj["shape_pt_lon"]
            self.shape_pt_sequence = obj["shape_pt_sequence"]
            self.shape_dist_traveled = obj["shape_dist_traveled"]
