import sys
import os
import json
from datetime import datetime

# Adjust the Python path to include the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from controllers.UserController import UserController

def main():
    """
    Fetches all users from the UserController and saves them to a JSON file
    named with the current date.
    """
    user_controller = UserController()
    
    print("Fetching all users...")
    users = user_controller.get_all_users()
    
    if not users:
        print("No users found.")
        return
        
    print(f"Found {len(users)} users.")
    
    # Define the output directory
    output_dir = os.path.join(project_root, 'output', 'user_reports')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with today's date
    today_date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"users-{today_date_str}.json"
    filepath = os.path.join(output_dir, filename)
    
    print(f"Saving users to {filepath}...")
    
    try:
        with open(filepath, 'w') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved users to {filepath}")
    except IOError as e:
        print(f"Error writing to file {filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
