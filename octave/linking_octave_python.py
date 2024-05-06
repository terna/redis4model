import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Example data
data = {'key1': 'value1', 'key2': 'value2'}

# Push data into Redis as a JSON string
r.set('data', json.dumps(data))