from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from tabs.project_manager import ProjectManagerTab
from tabs.another_tab import AnotherTab


# ToDo: Find a better import for tabs.


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep Visual Proteomics toolbox. Version: dev.0.0.1")  # ToDo: Add version
        self.init_ui()
        self.center_and_resize_window()

    def init_ui(self):
        # Create the tab widget and set it as the central widget of the main window
        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # Initialize tabs
        project_manager_tab = ProjectManagerTab(main_window=self)
        another_tab = AnotherTab(main_window=self)

        # Add tabs to the tab widget
        tabs.addTab(project_manager_tab, "Project Manager")
        tabs.addTab(another_tab, "Another Tab")

    def center_and_resize_window(self):
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.resize(size.width() // 2, size.height() // 2)
        rect = self.frameGeometry()
        center_point = screen.availableGeometry().center()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())

    def show_message(self, title, message, icon=QMessageBox.Information):
        """
        Displays a message box with the specified title, message, and icon.

        This function generalizes the message box display, allowing for various types of messages
        including information, warnings, errors, and success notifications, depending on the icon chosen.

        Parameters:
        - title (str): The title of the message box window.
        - message (str): The message to be displayed in the message box.
        - icon (QMessageBox.Icon, optional): The icon to be displayed in the message box. Defaults to
          QMessageBox.Information indicating an informational message. Other options include QMessageBox.Warning,
          QMessageBox.Critical, and QMessageBox.Question which can be used to indicate different types of messages.

        Returns:
        - None
        """
        message_box = QMessageBox(self)  # Parent the QMessageBox to the MainWindow
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
