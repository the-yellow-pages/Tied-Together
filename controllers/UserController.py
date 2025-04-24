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

    def get_liked_vehicles(self, user_id, page=None, limit=None):
        """
        Retrieve the vehicles liked by a specific user with pagination support.
        This method fetches all vehicle IDs liked by the user, applies pagination if requested,
        and returns the detailed vehicle information as a dictionary along with the total count.
        Args:
            user_id (int): The ID of the user whose liked vehicles are to be retrieved.
            page (int, optional): The page number for pagination. Defaults to None.
            limit (int, optional): The maximum number of items per page. Defaults to None.
        Returns:
            tuple: A tuple containing:
                - list: A list of dictionaries with vehicle details for the liked vehicles.
                - int: The total number of vehicles liked by the user.
        """
        all_ids = self.db.get_liked_vehicles(user_id)
        offset = (page - 1) * limit if page and limit else None
        paginated_ids = all_ids[offset:offset + limit] if offset is not None else all_ids
        
        # Extract the IDs from the tuples if they're in tuple format
        if paginated_ids and isinstance(paginated_ids[0], tuple):
            paginated_ids = [id_tuple[0] for id_tuple in paginated_ids]
            
        return self.db.make_dicts(self.db.read_liked_vehicles(paginated_ids)), len(all_ids)

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
        
    def add_disliked_vehicle(self, user: dict, vehicle_id):
        """
        tested
        Add a disliked vehicle for a user.
        :param user: dict with keys 'id', 'first_name', 'last_name', 'username'
        :param vehicle_id: int
        """
        user_db = self.get_user(user['id'])
        if not user_db:
            user_id = self.create_user(user)
        else:
            user_id = user['id']
        disliked_vehicle_data = {
            'user_id': user_id,
            'vehicle_id': vehicle_id
        }
        try:
            self.db.create_disliked_vehicle(disliked_vehicle_data)
            return disliked_vehicle_data
        except UniqueViolation as e:
            print(f"Vehicle with ID {vehicle_id} already disliked by user {user_id}. Error: {e}")
            return None
        

    def remove_liked_vehicle(self, user_id, vehicle_id, logger):
        """
        Remove a liked vehicle for a user.
        :param user_id: int
        :param vehicle_id: int
        """
        try:
            return self.db.delete_liked_vehicle(user_id, vehicle_id)
        except Exception as e:
            logger.error(f"Error removing liked vehicle: {e}")
            return None
