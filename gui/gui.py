from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox, QWidget
from tabs.project_manager import ProjectManagerTab
from tabs.add_files_tab import AddFilesTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep Visual Proteomics toolbox. Version: dev.0.0.1")
        self.init_ui()
        self.center_and_resize_window()

    def init_ui(self):
        # Create the tab widget and store it as an attribute
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize tabs
        self.project_manager_tab = ProjectManagerTab(main_window=self)
        self.add_files_tab = AddFilesTab(main_window=self)

        # Add tabs to the tab widget
        self.tabs.addTab(self.project_manager_tab, "Project Manager")
        self.add_files_tab_index = self.tabs.addTab(self.add_files_tab, "Add files")  # Store the index of the add files tab

        # Initially disable the Another Tab until a project is loaded
        self.tabs.setTabEnabled(self.add_files_tab_index, False)

    def center_and_resize_window(self):
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.resize(size.width() // 2, size.height() // 2)
        rect = self.frameGeometry()
        center_point = screen.availableGeometry().center()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())

    def show_message(self, title, message, icon=QMessageBox.Information):
        message_box = QMessageBox(self)
        message_box.setIcon(icon)
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def activate_add_files_tab(self):
        """Activates the add files tab after a project is loaded."""
        self.tabs.setTabEnabled(self.add_files_tab_index, True)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
