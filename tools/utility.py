import json
import pytz
from datetime import datetime

def generate_json_file(dictionary, file_directory):
    json_file_content = json.dumps(dictionary)
    with open(file_directory, 'w') as file:
        file.write(json_file_content)
    print(f'Exported: {file_directory}.json')

def get_local_time(location):
    local_timezone = pytz.timezone(location)
    local_time = datetime.now(local_timezone)
    return local_time

def update_log_file(log_message, file_directory):
    with open(file_directory, 'a') as file:
        file.write(log_message)

def log(start_log_message, finish_log_message):
    def log_decorator(func):
        def wrapper(*args, **kwargs):
            # Prepare Constants
            file_directory = 'logs/log.txt'
            location = 'Asia/Jakarta'
            timestamp_format = '%Y-%m-%d %H:%M:%S'

            # Get Start Time
            start_time = get_local_time(location)
            start_time_formatted = start_time.strftime(timestamp_format)

            # Log Start
            log_message = f'{start_time_formatted} {start_log_message}\n'
            update_log_file(log_message, file_directory)

            try:
                # Execute Function
                func(*args, **kwargs)


                # Get Finish Time
                finish_time = get_local_time(location)
                finish_time_formatted = finish_time.strftime(timestamp_format)

                # Get Duration
                duration = finish_time - start_time
                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                duration = f'{int(hours)}h {int(minutes)}m {int(seconds)}s'

                # Log Finish
                log_message = f'{finish_time_formatted} {finish_log_message} ({duration})\n'
                update_log_file(log_message, file_directory)
            
            except Exception as e:
                # Get Error Time
                error_time = get_local_time(location)
                error_time_formatted = error_time.strftime(timestamp_format)

                # Log Error
                log_message = f'{error_time_formatted} An error occured: {e}\n'
                update_log_file(log_message, file_directory)

        
        return wrapper
    return log_decorator