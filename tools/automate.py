# Imports
import os
import ast
import yaml
from datetime import datetime
import pytz

# Functions
def get_local_time(location):
    local_timezone = pytz.timezone(location)
    local_time = datetime.now(local_timezone)
    return local_time

def get_python_scripts(folder_directory):
    python_scripts = [file_name for file_name in os.listdir(folder_directory) if file_name.endswith('.py')]
    python_scripts.sort()
    return python_scripts

def get_requirements(python_script_list):
    # Get Built in Modules
    with open('tools/built_in_modules.txt', 'r') as file:
        built_in_modules = [module.strip() for module in file.readlines()]
    
    # Get External Modules
    external_modules = set()
    for script in python_script_list:
        with open(f'scripts/{script}', 'r') as file:
            tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if module_name not in built_in_modules:
                            external_modules.add(module_name)
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module.split('.')[0]
                    if module_name and node.module not in built_in_modules:
                        external_modules.add(module_name)
    
    external_modules = list(external_modules)
    external_modules.sort()
    return external_modules

def generate_requirements(requirement_list):
    with open('requirements.txt', 'w') as file:
        file_content = '\n'.join(requirement_list)
        file.write(file_content)

def generate_workflow_structure(python_script_list):
    python_script_list_no_extension = [script.split('.py')[0] for script in python_script_list]

    workflow_file_content = {
        'name': 'Update Database',
        'on': {
            'workflow_dispatch': {},
            'schedule': [
                {
                    'cron': '0 17 * * *'
                }
            ]
        },
        'jobs': {
            'run-python-scripts': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {
                        'name': 'Checkout Repository',
                        'uses': 'actions/checkout@v3'
                    },
                    {
                        'name': 'Set up Python',
                        'uses': 'actions/setup-python@v4',
                        'with': {
                            'python-version': '3.13.0'
                        }
                    },
                    {
                        'name': 'Install Dependencies',
                        'run': 'python -m pip install --upgrade pip && pip install -r scripts/requirements.txt'
                    },
                    {
                        'name': 'Create Directories',
                        'run': ' && '.join([f'if [ ! -d output/{name} ]; then mkdir -p output/{name}; fi' for name in python_script_list_no_extension])
                    },
                    {
                        'name': 'Run Python Scripts',
                        'run': ' && '.join([f'python scripts/{script}' for script in python_script_list])
                    },
                    {
                        'name': 'Set up Git User',
                        'run': 'git config --global user.name "github-actions[bot]" && git config --global user.email "github-actions[bot]@users.noreply.github.com"'
                    },
                    {
                        'name': 'Add Files to Git',
                        'run': ' && '.join([f'git add output/{name}/*' for name in python_script_list_no_extension])
                    },
                    {
                        'name': 'Commit Changes',
                        'run': 'git commit -m "Daily Database Update" || echo "No Changes to Commit"'
                    },
                    {
                        'name': 'Push Changes',
                        'run': 'git push'
                    }
                ]
            }
        }
    }

    return workflow_file_content

def generate_workflow_file(workflow_structure, file_directory):
    with open(file_directory, 'w') as file:
        yaml.dump(workflow_structure, file)

def update_log_file(log_message, file_directory):
    with open(file_directory, 'a') as file:
        file.write(log_message)

def log(item):
    def log_decorator(func):
        def wrapper():
            # Prepare Constants
            file_directory = 'logs/log.txt'
            location = 'Asia/Jakarta'
            timestamp_format = '%Y-%m-%d %H:%M:%S'

            # Get Start Time
            start_time = get_local_time(location)
            start_time_formatted = start_time.strftime(timestamp_format)

            # Log Start
            log_message = f'{start_time_formatted} Updating {item}...\n'
            update_log_file(log_message, file_directory)
            
            # Execute Function
            func()

            # Get Finish Time
            finish_time = get_local_time(location)
            finish_time_formatted = finish_time.strftime(timestamp_format)

            # Get Duration
            duration = finish_time - start_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            duration = f'{int(hours)}h {int(minutes)}m {int(seconds)}s'

            # Log Finish
            log_message = f'{finish_time_formatted} Finished Updating {item} ({duration})\n'
            update_log_file(log_message, file_directory)
        
        return wrapper
    return log_decorator

@log('Requirements')
def run_generate_requirements():
    python_script_list = get_python_scripts('scripts/')

    print('Generating requirements.txt')

    requirement_list = get_requirements(python_script_list)
    generate_requirements(requirement_list)

    print('Successfully generated requirements.txt')

@log('Workflow')
def run_generate_workflow():
    python_script_list = get_python_scripts('./')

    print('Generating execute_scripts.yml')

    workflow_structure = generate_workflow_structure(python_script_list)
    generate_workflow_file(workflow_structure, '.github/workflows/execute_scripts.yml')

    print('Successfully generated execute.yml')

def main():
    run_generate_requirements()
    run_generate_workflow()

if __name__ == '__main__':
    main()