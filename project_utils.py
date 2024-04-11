import os
from datetime import datetime
import pandas as pd
import yaml


def create_config_file(project_path: str, project_name: str) -> None:
    """
    Creates a config.yaml file and an HDF5 database file in the project directory with the project settings,
    including a timestamp of when the project was created, and the name of the database file.
    """
    config_path = os.path.join(project_path, 'config.yaml')
    database_path = os.path.join(project_path, f"{project_name}_database.hdf")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Project settings
    config = {
        'project_name': project_name,
        'project_directory': project_path,
        'creation_timestamp': current_time,
        'database_file': f"{project_name}_database.hdf"
    }

    # Write project settings to config.yaml
    with open(config_path, 'w') as config_file:
        yaml.dump(config, config_file)

    # Convert config to a DataFrame and store it in the HDF5 database
    config_df = pd.DataFrame(list(config.items()), columns=['Variable', 'Value'])
    config_df.to_hdf(database_path, key='config', mode='w')


def get_project_config(config_path: str) -> dict:
    """
    Returns the project configuration dictionary from a YAML file.
    """
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            return config if config else {}
    except Exception as e:
        print(f"Failed to load project configuration: {e}")
        return {}


def create_new_project(project_dir: str, project_name: str) -> None:
    """
    Creates a new project directory and an initial database file.
    """
    full_path = os.path.join(project_dir, project_name)
    try:
        os.makedirs(full_path, exist_ok=False)
    except FileExistsError:
        print(f"Project directory '{full_path}' already exists. Please choose a different name or location.")
        return

    # Create the initial config file and database
    create_config_file(full_path, project_name)
    print(f"Project '{project_name}' created at {project_dir}.")
