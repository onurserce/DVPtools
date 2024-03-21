from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QWidget
from project_utils import create_new_project


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Creator")

        # Setup central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Project name input
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name")
        layout.addWidget(self.project_name_input)

        # Button to create new project
        self.create_project_button = QPushButton("Create New Project")
        self.create_project_button.clicked.connect(self.on_create_new_project)
        layout.addWidget(self.create_project_button)

    def on_create_new_project(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_dir:
            project_name = self.project_name_input.text()
            create_new_project(project_dir, project_name)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
