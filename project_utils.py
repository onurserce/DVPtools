import os
from datetime import datetime
import yaml


def create_config_file(project_path: str, project_name: str) -> None:
    """
    Creates a config.yaml file in the project directory with the project settings,
    including a timestamp of when the project was created.

    Parameters:
    - project_path (str): The full path to the project directory.
    - project_name (str): The name of the project.
    """
    config_path = os.path.join(project_path, 'config.yaml')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Project settings
    config = {
        'project_name': project_name,
        'project_directory': project_path,
        'creation_timestamp': current_time,
    }

    with open(config_path, 'w') as config_file:
        yaml.dump(config, config_file)


def create_new_project(project_dir: str, project_name: str) -> None:
    """
    Creates a new project directory.

    Parameters:
    - project_dir (str): The directory where the project will be created.
    - project_name (str): The name of the project.
    """
    if not project_name:
        project_name = "NewProject"  # Default project name

    full_path = os.path.join(project_dir, project_name)
    os.makedirs(full_path, exist_ok=True)

    # Separately create the initial config file
    create_config_file(full_path, project_name)

    print(f"Project '{project_name}' created at {project_dir}")
