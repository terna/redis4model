for i = 1:5
    % Wait until Python has sent data
    while true
        [status, data] = system('/opt/homebrew/bin/redis-cli get python_to_octave');
        if status == 0 && !isempty(strtrim(data))
            break;
        endif
        pause(1); % Wait before checking again
    end
    
    % Process data
    printf("Octave received: %s\n", strtrim(data)); 
    
    % Clear the python_to_octave key to avoid stale reads
    system('/opt/homebrew/bin/redis-cli del python_to_octave');
    
    % Send result back to Redis
    index = strfind(data, num2str(i-1));
    index_start = strfind(data, "Start");
    if !isempty(index) || !isempty(index_start)
        result = strcat("Octave ", num2str(i));
        printf('Octave computing...')
        pause(5);
        printf("Octave sending: %s\n", result);
        redis_command = ['echo "', result, '" | /opt/homebrew/bin/redis-cli -x set octave_to_python'];
        system(redis_command);
    end

end
