from models import Model


class AgencyModel(Model):
    def __init__(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS agency (" \
                             "agency_id   bigint," \
                             "agency_name text  ," \
                             "agency_url  text  ," \
                             "PRIMARY KEY (agency_id))"
        insert_query = "INSERT INTO agency (agency_id, agency_name, agency_url) " \
                       "VALUES (%(agency_id)s, %(agency_name)s, %(agency_url)s) " \
                       "IF NOT EXISTS"
        read_all_query = "SELECT * FROM agency"
        count_all_query = "SELECT COUNT(*) FROM agency"
        fields = ["agency_id", "agency_name", "agency_url"]
        super().__init__(create_table_query, insert_query, read_all_query, count_all_query, fields, Agency)


class Agency:
    def __init__(self, obj=None):
        if obj is not None:
            self.agency_id = obj["agency_id"]
            self.agency_name = obj["agency_name"]
            self.agency_url = obj["agency_url"]
