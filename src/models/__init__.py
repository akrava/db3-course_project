from cassandra.cluster import Cluster


class SingletonMeta(type):
    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class CassandraClient(metaclass=SingletonMeta):
    def __init__(self):
        self.__cluster = Cluster()
        self.__session = self.__cluster.connect()
        if "db3_course_project" not in self.__cluster.metadata.keyspaces:
            self.__session.execute("CREATE KEYSPACE db3_course_project WITH replication = "
                                   "{'class': 'SimpleStrategy', 'replication_factor':2}")
        self.__session.execute("USE db3_course_project")

    def get_session(self):
        return self.__session

    def get_cluster(self):
        return self.__cluster


class Model:
    def __init__(self, create_table_query: str, create_query: str, read_all_query: str,
                 count_all_query: str, fields: [str], cls):
        self._session = self._get_session()
        self._create_query = create_query
        self._read_all_query = read_all_query
        self._count_all_query = count_all_query
        self._fields = fields
        self._cls = cls
        self._session.execute(create_table_query)

    @staticmethod
    def _get_session():
        return CassandraClient().get_session()

    def create(self, obj):
        try:
            self._session.execute(self._create_query, self._convert_obj_to_params(obj))
        except Exception as e:
            print(e)
            return False
        return True

    def read_all(self):
        try:
            res = self._session.execute(self._read_all_query)
        except Exception as e:
            print(e)
            return False
        return [self._convert_row_to_obj(row) for row in res.all()]

    def count_all(self):
        try:
            res = self._session.execute(self._count_all_query)
        except Exception as e:
            print(e)
            return False
        return res.one().count

    def _convert_obj_to_params(self, obj):
        res = dict()
        for field in self._fields:
            res[field] = getattr(obj, field)
        return res

    def _convert_row_to_obj(self, row):
        res = self._cls()
        for field in self._fields:
            setattr(res, field, getattr(row, field))
        return res
