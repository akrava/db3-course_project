
class VehiclePosition:
    def __init__(self, feed_entity):
        self.id = feed_entity.id
        vehicle_obj = feed_entity.vehicle
        self.route_id = vehicle_obj.trip.route_id
        self.trip_id = vehicle_obj.trip.trip_id
        self.latitude = vehicle_obj.position.latitude
        self.longitude = vehicle_obj.position.longitude
        self.speed = vehicle_obj.position.speed
        self.bearing = vehicle_obj.position.bearing
        self.odometer = vehicle_obj.position.odometer
        self.timestamp = vehicle_obj.timestamp
        self.vehicle_id = vehicle_obj.vehicle.id
        self.license_plate = vehicle_obj.vehicle.license_plate