from database.User import UsersDB
from psycopg2.errors import UniqueViolation


class UserController:
    def __init__(self):
        self.db = UsersDB()
        
    def create_user(self, user_data):
        """
        Create a new user.
        :param user_data: dict with keys 'id', 'first_name', 'last_name', 'username'
        """
        try:
            return self.db.create_user(user_data)
        except UniqueViolation as e:
            print(f"User with ID {user_data['id']} already exists. Error: {e}")
            return None

    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        :param user_id: int
        """
        # return self.db.read_user(user_id)
        return self.db.make_dict(self.db.read_user(user_id))

    def update_user(self, user_id, updated_data):
        """
        Update user details.
        :param user_id: int
        :param updated_data: dict with keys to update (e.g., 'first_name', 'last_name', 'username')
        """
        self.db.update_user(user_id, updated_data)

    def delete_user(self, user_id):
        """
        Delete a user by ID.
        :param user_id: int
        """
        self.db.delete_user(user_id)

    def get_liked_vehicles(self, user_id):
        """
        Retrieve all liked vehicles for a user by joining of all tables.
        :param user_id: int
        """
        return self.db.make_dicts(self.db.read_liked_vehicles(user_id))

    def add_liked_vehicle(self, user: dict, vehicle_id: int):
        """
        Add a liked vehicle for a user. creates user if not exists
        :param user: dict with keys 'id', 'first_name', 'last_name', 'username'
        :param vehicle_id: int
        """
        user_db = self.get_user(user['id'])
        if not user_db:
            user_id = self.create_user(user)
        else:
            user_id = user['id']
        liked_vehicle_data = {
            'user_id': user_id,
            'vehicle_id': vehicle_id
        }
        try:
            self.db.create_liked_vehicle(liked_vehicle_data)
            return liked_vehicle_data
        except UniqueViolation as e:
            print(f"Vehicle with ID {vehicle_id} already liked by user {user_id}. Error: {e}")
            return None
        

    def remove_liked_vehicle(self, user_id, vehicle_id):
        """
        Remove a liked vehicle for a user.
        :param user_id: int
        :param vehicle_id: int
        """
        self.db.delete_liked_vehicle(user_id, vehicle_id)
