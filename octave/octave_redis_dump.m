% Create random data
random_data = rand(1, 10);

% Convert data to string (Redis stores data as strings)
data_str = sprintf('%.4f ', random_data);

% Write data to Redis using system command
redis_key = 'octave_random_data';
redis_command = ['echo "', data_str, '" | /opt/homebrew/bin/redis-cli -x set ', redis_key];
system(redis_command);

disp(data_str)

