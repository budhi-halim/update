import os
import yaml

def main():
    print('Updating execute_scripts.yml')
    python_scripts = [file_name for file_name in os.listdir('./') if file_name.endswith('.py')]

    #Create YAML File
    yaml_file_content = {
        'name': 'Update Database',
        'on': {
            'workflow_dispatch': {},
            'push': {
                'branches': ['main']
            },
            'schedule': [
                {
                    'cron': '*/15 * * * *'
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
                        'name': 'List Requirements',
                        'run': 'pip freeze > requirements.txt'
                    },
                    {
                        'name': 'Install Dependencies',
                        'run': 'python -m pip install --upgrade pip && pip install -r requirements.txt'
                    },
                    {
                        'name': 'Run Python Scripts',
                        'run': ' && '.join([f'python {script}' for script in python_scripts])
                    },
                    {
                        'name': 'Create Download Directories',
                        'run': ' && '.join([f'mkdir - output/{script[:-3]}' for script in python_scripts])
                    },
                    {
                        'name': 'Set up Git User',
                        'run': 'git config --global user.name "github-actions[bot]" && git config --global user.email "github-actions[bot]@users.noreply.github.com"'
                    },
                    {
                        'name': 'Add Files to Git',
                        'run': ' && '.join([f'git add output/{script[:-3]}/*' for script in python_scripts])
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

    with open('.github/workflows/execute_scripts.yml', 'w') as file:
        yaml.dump(yaml_file_content, file, default_flow_style=False)
    
    print('Successfully updated execute_scripts.yml')

if __name__ == '__main__':
    main()