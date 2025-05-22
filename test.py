from database.Vehicles import VehiclesDB
from database.User import UsersDB
from controllers.UserController import UserController

#vehicle_ID: 403989866
if __name__ == "__main__":
    user = UsersDB()
    controller = UserController()
    ids = user.get_liked_vehicles(200692606)
    print(len(ids))
    print(ids, '\ndone')
    cars, count = controller.get_liked_vehicles(200692606, 1, 3)
    print("\nCOUNT :", count)
    for car in cars:
        print(car.get("vehicle_id", 0))
    # user_data = {
    #     'id': 400,    
    #     'first_name': 'Test',
    #     'last_name': 'User',
    #     'username': 'testuser'
    # }
    # vehicle_id = 403989866
    # res = controller.create_user(user_data)
    # print(res)
    # res = controller.get_user(user_data['id'])
    # print(res)
    # res = controller.get_user(1)
    # print(res)
    # res = controller.add_liked_vehicle(user_data, vehicle_id)
    # print(res)
    # res = controller.add_liked_vehicle(user_data, 378940062)
    # print(res)
    # res = controller.remove_liked_vehicle(user_data['id'], vehicle_id)
    # res = controller.get_liked_vehicles(user_data['id'])
    # print(res)