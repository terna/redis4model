import redis
import random

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Generate random data
random_data = [round(random.random(), 4) for _ in range(10)]

# Convert data to string
data_str = ' '.join(map(str, random_data))

# Set data in Redis
redis_key = 'random_data'
r.set(redis_key, data_str)

print(f"Data written to Redis: {data_str}")