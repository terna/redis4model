data_str = 'Data from Octave';
redis_key = 'octave_data';
redis_command = ['echo "', data_str, '" | /opt/homebrew/bin/redis-cli -x set ', redis_key];
pause(30);
system(redis_command);