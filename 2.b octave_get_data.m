redis_key = 'python_data';

% Construct the command to get the value from Redis
redis_command = ['/opt/homebrew/bin/redis-cli get ', redis_key];

% Execute the command and capture the output
[status, result] = system(redis_command);

% Check if the command was successful
if status == 0
    % The command was successful, and the result contains the data
    fetched_data = result;
    disp('Fetched Python data from Redis:');
    disp(fetched_data);
else
    % The command failed
    disp('Failed to fetch Python data from Redis.');
end