from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QWidget, \
    QMessageBox
from project_utils import create_new_project


def show_success_message(project_name: str, project_dir: str):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Information)
    message_box.setWindowTitle("Project Created")
    message_box.setText(f"Project '{project_name}' has been successfully created at:\n{project_dir}")
    message_box.setStandardButtons(QMessageBox.Ok)
    message_box.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Creator")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Enter project name")
        layout.addWidget(self.project_name_input)

        self.create_project_button = QPushButton("Create New Project")
        self.create_project_button.clicked.connect(self.on_create_new_project)
        layout.addWidget(self.create_project_button)

    def on_create_new_project(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_dir:
            project_name = self.project_name_input.text()
            create_new_project(project_dir, project_name)
            show_success_message(project_name, project_dir)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
