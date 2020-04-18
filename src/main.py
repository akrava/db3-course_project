from cassandra.cluster import Cluster


if __name__ == "__main__":
    cluster = Cluster()
    session = cluster.connect()
    print("course project")
    print(cluster.client_id)
