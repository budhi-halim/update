from utility import generate_json_file, get_local_time, update_log_file

def log_start(start_log_message):
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