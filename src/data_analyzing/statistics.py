from models.vehicle_position import VehiclePositionModel
from models.routes import RoutesModel
from data_processing.realtime_information import GTFSRealtime


class General:
    @staticmethod
    def get_all_speeds():
        model = VehiclePositionModel()
        all_speeds = model.get_all_speeds()
        return [x for x in all_speeds if x > 0]

    @staticmethod
    def count_types_vehicle():
        model = VehiclePositionModel()
        routes_model = RoutesModel()
        vehicles = model.read_all()
        distinct_vehicles = GTFSRealtime.get_distinct_by_keys(vehicles, ['vehicle_id'], lambda x, y: True)
        count_tram = 0
        cont_bus = 0
        count_others = 0
        count_trolley = 0
        for vehicle in distinct_vehicles:
            route = routes_model.get_route_by_id(int(vehicle.route_id))
            if route.route_type == 0:
                count_tram = count_tram + 1
            elif route.route_type == 3:
                if route.route_short_name.startswith('А'):
                    cont_bus = cont_bus + 1
                elif route.route_short_name.startswith('Тр'):
                    count_trolley = count_trolley + 1
                else:
                    count_others = count_others + 1
            else:
                count_others = count_others + 1
        return {
            "трамвай": count_tram,
            "автобус": cont_bus,
            "тролейбус": count_trolley
        }
