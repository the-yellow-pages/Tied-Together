import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

URL = "http://localhost:5000/api/getnextcandidate"  # Adjust if needed

def make_request(user_id):
    # Generate random price range (ensuring start < end)
    start_price = random.randint(5000, 50000)
    end_price = random.randint(start_price, 100000)

    # Generate random year range (ensuring start < end)
    start_year = random.randint(1980, 2015)
    end_year = random.randint(start_year, 2023)

    payload = {
        "user": {"id": user_id},
        "start_price": start_price,
        "end_price": end_price,
        "start_year": start_year,
        "end_year": end_year,
        "limit": 10
    }
    start = time.time()
    try:
        response = requests.post(URL, json=payload, timeout=40)
        elapsed = time.time() - start
        # Improved error reporting for server errors
        if response.status_code >= 500:
            print(f"Server error for user {user_id}: {response.status_code} - {response.text}")
        return (response.status_code, elapsed)
    except Exception as e:
        print(f"Request failed for user {user_id}: {e}")
        return ("error", 0)

def run_load_test(concurrent_users):
    print(f"\nTesting with {concurrent_users} concurrent users...")
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = [executor.submit(make_request, i+1) for i in range(concurrent_users)]
        results = [f.result() for f in as_completed(futures)]
    status_counts = {}
    total_time = 0
    for status, elapsed in results:
        status_counts[status] = status_counts.get(status, 0) + 1
        total_time += elapsed
    avg_time = total_time / concurrent_users
    print(f"Status codes: {status_counts}")
    print(f"Average response time: {avg_time:.3f} seconds")
    print(f"Total time taken: {total_time:.3f} seconds")

if __name__ == "__main__":
    run_load_test(15)
