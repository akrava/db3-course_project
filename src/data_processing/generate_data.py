import sys
import time
from data_processing.realtime_information import GTFSRealtime
from data_processing.static_information import GTFSStatic
from models.vehicle_position import VehiclePositionModel


def generate_data():
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        if len(sys.argv) == 2 and sys.argv[1] == "--static":
            print("Saving static GTFS information to DB")
            gtfs = GTFSStatic()
            gtfs.save_static_info_to_db()
        elif len(sys.argv) == 3 and sys.argv[1] == "--dynamic":
            timeout = sys.argv[2]
            if not timeout.isdigit() or int(timeout) <= 0:
                print("Timeout must be > 0")
                sys.exit(1)
            timeout = int(timeout)
            print(f"Saving dynamic GTFS information to DB with timeout {timeout}")
            gtfs = GTFSRealtime()
            model = VehiclePositionModel()
            while True:
                print("Trying to save feed...")
                gtfs.save_current_feed_to_db()
                count = model.count_all()
                print(f'Count: {count}')
                print("Saved. Timeout...")
                time.sleep(timeout)
        else:
            print("Unknown argument")
    else:
        print("Provide mode --dynamic N or --static with command arguments")
        sys.exit(1)
