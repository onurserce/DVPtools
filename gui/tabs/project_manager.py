from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
from project_utils import create_new_project, get_project_config
from os import path


class ProjectManagerTab(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.on_reset()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Project info label
        self.project_info_label = QLabel("No project loaded. Please load an existing project or create a new one.")
        layout.addWidget(self.project_info_label)

        # New project group
        new_project_group = QGroupBox("New Project")
        new_project_layout = QVBoxLayout(new_project_group)
        self.select_dir_button = QPushButton("Select Project Directory")
        self.select_dir_button.clicked.connect(self.on_select_directory)
        self.selected_dir_label = QLabel("Selected directory: None")
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name")
        self.create_project_button = QPushButton("Create New Project")
        self.create_project_button.clicked.connect(self.on_create_new_project)
        new_project_layout.addWidget(self.select_dir_button)
        new_project_layout.addWidget(self.selected_dir_label)
        new_project_layout.addWidget(self.project_name_input)
        new_project_layout.addWidget(self.create_project_button)
        layout.addWidget(new_project_group)

        # Load project group
        load_project_group = QGroupBox("Load Project")
        load_project_layout = QVBoxLayout(load_project_group)
        self.load_project_button = QPushButton("Load Project")
        self.load_project_button.clicked.connect(self.on_load_project)
        load_project_layout.addWidget(self.load_project_button)
        layout.addWidget(load_project_group)

        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.on_reset)
        layout.addWidget(self.reset_button)

    def on_select_directory(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_dir:
            self.selected_directory = project_dir
            self.selected_dir_label.setText(f"Selected directory: {project_dir}")
            self.update_ui_state(directory_selected=True)

    def on_create_new_project(self):
        if self.selected_directory:
            project_name = self.project_name_input.text()
            if project_name:
                try:
                    create_new_project(self.selected_directory, project_name)
                    # Successfully created the project, now load it
                    self.load_project(path.join(self.selected_directory, project_name, "config.yaml"))
                    # Inform the user that the project has been created and loaded
                    self.main_window.show_message(
                        title="Project Created",
                        message=f"Project '{project_name}' has been successfully created and loaded.",
                        icon=QMessageBox.Information)
                except FileExistsError as err:
                    self.main_window.show_message(
                        title="Project already exists",
                        message=str(err) + "\n\nPlease choose another name or location for your project",
                        icon=QMessageBox.Critical)
                    return
            else:
                QMessageBox.warning(self, "Project Name Required", "Please enter a project name.")

    def on_load_project(self):
        config_path = QFileDialog.getOpenFileName(self, "Select config.yaml", "", "YAML Files (*.yaml *.yml)")[0]
        if config_path:
            self.load_project(config_path)
            # Assuming load_project updates self.config with the loaded project's name
            if self.config:
                project_name = self.config.get('project_name', 'Unknown Project')
                self.main_window.show_message(
                    title="Project Loaded",
                    message=f"Project '{project_name}' has been successfully loaded.",
                    icon=QMessageBox.Information)
        else:
            QMessageBox.warning(self, "Load Project", "No config file selected.")

    def on_reset(self):
        self.selected_directory = None
        self.config = None
        self.update_ui_state(reset=True)

    def load_project(self, config_path: str):
        self.config = get_project_config(config_path)
        if self.config:
            self.project_name = self.config.get('project_name', 'Unknown Project')
            self.project_directory = self.config.get('project_directory', 'Unknown Directory')
            self.creation_timestamp = self.config.get('creation_timestamp', 'Unknown Timestamp')
            self.selected_directory = self.project_directory
            self.update_ui_state(project_loaded=True)
        else:
            QMessageBox.warning(self, "Load Project", "Failed to load the project.")
            raise Exception

    def update_ui_state(self, reset=False, directory_selected=False, project_loaded=False):
        """Updates the UI state based on the user action."""
        if reset:
            self.project_name_input.clear()
            self.selected_dir_label.setText("Selected directory: None")
            self.project_info_label.setText("No project loaded. Please load an existing project or create a new one.")
            self.project_name_input.setEnabled(False)
            self.create_project_button.setEnabled(False)
            self.select_dir_button.setEnabled(True)
            self.load_project_button.setEnabled(True)
        elif directory_selected:
            self.project_name_input.setEnabled(True)
            self.create_project_button.setEnabled(True)
            self.select_dir_button.setEnabled(False)  # Optional: disable if you don't want directory reselection
            self.load_project_button.setEnabled(False)
        elif project_loaded:
            self.project_name_input.setEnabled(False)
            self.create_project_button.setEnabled(False)
            self.select_dir_button.setEnabled(False)
            self.load_project_button.setEnabled(False)
            self.reset_button.setEnabled(True)
            self.main_window.activate_add_files_tab()

            # Update the project info label using the current configuration
            if self.config:
                project_name = self.config.get('project_name', 'Unknown Project')
                project_directory = self.config.get('project_directory', 'Unknown Directory')
                creation_timestamp = self.config.get('creation_timestamp', 'Unknown Timestamp')
                self.project_info_label.setText(
                    f"Project Name: {project_name}\n"
                    f"Directory: {project_directory}\n"
                    f"Created: {creation_timestamp}")
