import redis
import time

# Connect to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushdb()

# Send start message to Octave
r.set("python_to_octave", "Start")

for i in range(5):
    
    # Wait until Octave has set data
    while r.get("octave_to_python") is None:
        time.sleep(1)

    # Read Octave's data
    data = r.get("octave_to_python").decode('utf-8')
    print(f"Python received: {data}")

    # Clear the octave_to_python key to avoid stale reads
    r.delete("octave_to_python")

    # Send result back to Redis
    if str(i+1) in data:
        result = f'Python {i+1}'
        print('Python computing...')
        time.sleep(5)
        print(f"Python sending: {result}")
        r.set("python_to_octave", result)