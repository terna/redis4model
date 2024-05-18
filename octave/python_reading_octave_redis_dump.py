import redis
import random
import time

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Function to write data to Redis
def write_data():
    random_data = [round(random.random(), 4) for _ in range(10)]
    data_str = ' '.join(map(str, random_data))
    redis_key = 'python_random_data'
    r.set(redis_key, data_str)
    print(f"Python wrote: {data_str}")

# Function to read data from Redis
def read_data():
    redis_key = 'octave_random_data'
    data_str = r.get(redis_key)
    if data_str:
        print(f"Python read: {data_str.decode('utf-8')}")
    else:
        print("No data found from Octave")

# Write and read data
write_data()
time.sleep(1)  # Wait for Octave to write data
read_data()
