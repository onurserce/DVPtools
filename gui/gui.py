from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QWidget, \
    QMessageBox, QLabel
from project_utils import create_new_project


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Creator")
        self.selected_directory = None  # To store the selected directory path

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Button to select the project directory
        self.select_dir_button = QPushButton("Select Project Directory")
        self.select_dir_button.clicked.connect(self.on_select_directory)
        layout.addWidget(self.select_dir_button)

        # Label to display the selected project directory
        self.selected_dir_label = QLabel("Selected directory: None")
        layout.addWidget(self.selected_dir_label)

        # Input for the project name becomes active after directory selection
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name")
        self.project_name_input.setEnabled(False)  # Disabled initially
        layout.addWidget(self.project_name_input)

        # Button to create the project, active only after directory selection
        self.create_project_button = QPushButton("Create New Project")
        self.create_project_button.clicked.connect(self.on_create_new_project)
        self.create_project_button.setEnabled(False)  # Disabled initially
        layout.addWidget(self.create_project_button)

    def on_select_directory(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_dir:
            self.selected_directory = project_dir
            self.selected_dir_label.setText(f"Selected directory: {project_dir}")
            # Enable project name input and create project button
            self.project_name_input.setEnabled(True)
            self.create_project_button.setEnabled(True)
        else:
            # Reset if no directory is selected
            self.selected_directory = None
            self.selected_dir_label.setText("Selected directory: None")
            self.project_name_input.setEnabled(False)
            self.create_project_button.setEnabled(False)

    def on_create_new_project(self):
        if self.selected_directory:
            project_name = self.project_name_input.text()
            if project_name:  # Check if the project name is not empty
                create_new_project(self.selected_directory, project_name)
                show_message(
                    title='Project Created',
                    message=f"Project '{project_name}' has been successfully created at:\n{self.selected_directory}",
                    icon=QMessageBox.Information
                )
            else:
                # Inform the user that project name is required
                QMessageBox.warning(self, "Project Name Required", "Please enter a project name.")
        else:
            # This condition may not be necessary if the button is disabled correctly
            QMessageBox.warning(self, "Directory Not Selected", "Please select a project directory first.")


def show_message(title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Information) -> None:
    """
    Displays a message box with the specified title, message, and icon.

    This function generalizes the message box display, allowing for various types of messages
    including information, warnings, errors, and success notifications, depending on the icon chosen.

    Parameters:
    - title (str): The title of the message box window.
    - message (str): The message to be displayed in the message box.
    - icon (QMessageBox.Icon, optional): The icon to be displayed in the message box. Defaults to
      QMessageBox.Information indicating an informational message. Other options include QMessageBox.Warning,
      QMessageBox.Error, and QMessageBox.Question which can be used to indicate different types of messages.

    Returns:
    - None
    """
    message_box = QMessageBox()
    message_box.setIcon(icon)
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.Ok)
    message_box.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
