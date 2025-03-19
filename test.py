from database.Vehicles import VehiclesDB


if __name__ == "__main__":
    vehicles = VehiclesDB()
    res = vehicles.get_hundred_vehicle()
    print(res[0])
    print(len(res))
    