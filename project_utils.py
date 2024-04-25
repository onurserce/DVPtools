import os
import yaml
from datetime import datetime
from typing import Dict


class ProjectConfig:
    def __init__(self, project_name: str, project_dir: str, load_from_disk: bool = False):
        """
        Initializes the ProjectConfig object, either by creating new configuration
        or by loading an existing configuration from disk.

        Args:
        project_name (str): The name of the project.
        project_dir (str): The directory in which to place the project folder.
        load_from_disk (bool, optional): Flag to indicate if configuration should
                                         be loaded from disk instead of creating
                                         a new one. Defaults to False.
        """
        if not load_from_disk:
            # Class attributes
            self.project_name = project_name
            self.project_directory = os.path.join(project_dir, project_name)
            self.creation_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.config_path = os.path.join(self.project_directory, 'config.yaml')
            self.database_path = os.path.join(self.project_directory, 'database.h5')

            os.mkdir(self.project_directory)
        else:
            self.load_config(project_name, project_dir)

        self.save_config()

    def get_config(self) -> Dict[str, str]:
        """
        Returns the config variables in a dictionary
        """
        config = vars(self)
        return config

    def set_config(self, config: Dict[str, str]):
        """
        Sets the configuration attributes based on the provided dictionary. If the
        attribute does not exist, it will be created.

        Args:
        config (Dict[str, str]): A dictionary with configuration key-value pairs.
        """
        for key, value in config.items():
            # Check if the attribute exists in the class and update it
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                # Handle or ignore extra attributes
                setattr(self, key, value)
                print(f"Adding a new attribute '{key}' from the config")

    def save_config(self):
        """
        Saves the current configuration file to disk.
        """
        config = self.get_config()
        with open(self.config_path, 'w') as config_file:
            yaml.dump(config, config_file)

    def load_config(self, project_name: str, project_dir: str):
        """
        Loads the configuration from a YAML file into the project attributes.

        Args:
        project_name (str): The name of the project.
        project_dir (str): The directory where the project folder is located.
        """
        self.config_path = os.path.join(project_dir, project_name, 'config.yaml')
        with open(self.config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        self.set_config(config)
