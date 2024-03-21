import os
import yaml


def create_new_project(project_dir: str, project_name: str):
    """
    Creates a new project directory and a config.yaml file with project settings.

    Parameters:
    - project_dir: The directory where the project will be created.
    - project_name: The name of the project.
    """
    if not project_name:
        project_name = "NewProject"  # Default project name

    full_path = os.path.join(project_dir, project_name)
    config_path = os.path.join(full_path, 'config.yaml')
    os.makedirs(full_path, exist_ok=True)

    # Write project settings to config.yaml
    config = {
        'project_name': project_name,
        'project_directory': full_path
    }
    with open(config_path, 'w') as config_file:
        yaml.dump(config, config_file)

    print(f"Project '{project_name}' created at {project_dir}")
