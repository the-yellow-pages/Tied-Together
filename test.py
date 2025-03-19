from database.Vehicles import VehiclesDB


if __name__ == "__main__":
    vehicles = VehiclesDB()
    print(type(vehicles.get_big_capacity()))
    for vehicle in vehicles.get_big_capacity():
        print(vehicle)
        print("____________________")
    