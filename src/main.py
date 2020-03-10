from cassandra.cluster import Cluster
from data_processing.vehicle_positions import GTFSRealtime, VehiclePosition
from data_processing.static_information import GTFSStatic
from dotenv import load_dotenv, find_dotenv
import time

load_dotenv(find_dotenv())


if __name__ == "__main__":
    cluster = Cluster()
    session = cluster.connect()
    print("course project")
    print(cluster.client_id)

    hh = GTFSStatic()
    hh.save_zip()
    g = hh.parse()

    for index, row in g["stop_times"].iterrows():
        print(row.get("trip_id"))
        print()
        print(row)
        break

    # for i in range(0, 1000):
    #     v = FeedMessages()
    #     d = v.get_bytes()
    #     entities = v.parse(d)
    #     print(len(entities))
    #     filtered = v.filter_data(entities)
    #     print(len(filtered))
    #     g = [VehiclePosition(x) for x in filtered]
    #     print(len(g))
    #     #print(filtered[0])
    #     if "db3_course_project" not in cluster.metadata.keyspaces:
    #         session.execute("CREATE KEYSPACE db3_course_project WITH replication = {'class': 'SimpleStrategy', 'replication_factor':2}")
    #     session.execute("USE db3_course_project")
    #     session.execute("CREATE TABLE IF NOT EXISTS vehicle_position ("
    #                     "id             bigint   ,"
    #                     "route_id       text     ,"
    #                     "trip_id        text     ,"
    #                     "latitude       double   ,"
    #                     "longitude      double   ,"
    #                     "speed          double   ,"
    #                     "bearing        double   ,"
    #                     "odometer       double   ,"
    #                     "timestamp      timestamp,"
    #                     "vehicle_id     text     ,"
    #                     "license_plate  text     ,"
    #                     "PRIMARY KEY (id, timestamp)) WITH CLUSTERING ORDER BY (timestamp DESC)")
    #     for hmm in g:
    #         print(f'{int(hmm.id) + hmm.timestamp} {hmm.timestamp} {hmm.latitude}')
    #         session.execute("INSERT INTO vehicle_position (id, route_id, trip_id, latitude, longitude, speed, bearing, odometer, timestamp, vehicle_id, license_plate) VALUES (%(id)s, %(route_id)s, %(trip_id)s, %(latitude)s, %(longitude)s, %(speed)s, %(bearing)s, %(odometer)s, %(timestamp)s, %(vehicle_id)s, %(license_plate)s) IF NOT EXISTS", {
    #             "id": int(hmm.id) + hmm.timestamp,
    #             "route_id": hmm.route_id,
    #             "trip_id": hmm.trip_id,
    #             "latitude": hmm.latitude,
    #             "longitude": hmm.longitude,
    #             "speed": hmm.speed,
    #             "bearing": hmm.bearing,
    #             "odometer": hmm.odometer,
    #             "vehicle_id": hmm.vehicle_id,
    #             "license_plate": hmm.license_plate,
    #             "timestamp": hmm.timestamp,
    #         })
    #     print(session.execute("SELECT COUNT(*) as coun FROM vehicle_position").one())
    #     time.sleep(3)
    #
    # r = session.execute("SELECT * FROM vehicle_position")
    # for x in r:
    #     print(x)
