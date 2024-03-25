import pandas as pd
import logging
from PySide6.QtWidgets import (QApplication, QFileDialog, QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox,
                               QScrollArea, QWidget, QMainWindow, QTabWidget, QPushButton)

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='bad_lines.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def select_file() -> str:
    """
    Opens a system dialog window for the user to select a file.
    Returns the absolute path of the selected file.

    Returns:
    - str: The absolute path of the selected file. Returns an empty string if no file is selected.
    """
    app = QApplication.instance()  # Checks if QApplication already exists
    if not app:  # If not, create a new QApplication
        app = QApplication([])

    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    if file_dialog.exec():
        file_path = file_dialog.selectedFiles()[0]  # Gets the selected file path
        return file_path
    return ""  # Returns an empty string if no file is selected


def handle_bad_line(bad_line: list[str]) -> None:
    """
    Handles logging of bad lines encountered while reading a CSV file.

    Parameters:
    - bad_line (list[str]): The bad line encountered during CSV reading.
    """
    logger.warning(f"Bad line skipped: {bad_line}")


def read_csv_with_logging(file_path: str) -> pd.DataFrame:
    """
    Reads a ";" seperated .csv file into a DataFrame while handling bad lines by skipping and logging them to a file.

    Parameters:
    - file_path (str): The path to the .csv file to be read.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing the data from the .csv file.
    """
    try:
        # Attempt to read the CSV with a custom function to handle bad lines
        df = pd.read_csv(file_path, sep=",", on_bad_lines=handle_bad_line, engine="python")
        logger.info(f"CSV file '{file_path}' read successfully.")
        return df
    except Exception as e:
        # Log any errors encountered during the read process
        logger.error(f"Failed to read CSV file '{file_path}': {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error


def select_columns(df: pd.DataFrame) -> list:
    """
    Opens a dialog window for the user to select DataFrame columns to keep.

    Parameters:
    - df (pd.DataFrame): The DataFrame from which columns can be selected.

    Returns:
    - list: A list of selected column names.
    """
    app = QApplication.instance()
    if not app:  # If not, create a new QApplication
        app = QApplication([])

    class ColumnSelectorDialog(QDialog):
        def __init__(self, columns):
            super().__init__()
            self.setWindowTitle('Select Columns')
            self.selected_columns = []

            # Create a scroll area to hold the checkboxes if there are many columns
            scroll_area = QScrollArea(self)
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            # Create a checkbox for each column
            self.checkboxes = []

            for col in columns:
                checkbox = QCheckBox(col)
                self.checkboxes.append(checkbox)
                scroll_layout.addWidget(checkbox)

            # Finalize the scroll area setup
            scroll_widget.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_widget)

            # Layout for the dialog itself
            main_layout = QVBoxLayout(self)
            main_layout.addWidget(scroll_area)

            # Button box for OK and Cancel
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            main_layout.addWidget(button_box)

        def accept(self):
            # Gather the selected columns
            self.selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
            super().accept()

    # Create and show the dialog
    dialog = ColumnSelectorDialog(df.columns)
    if dialog.exec():
        return dialog.selected_columns
    else:
        return []  # Return an empty list if the dialog is canceled


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CSV Data Analysis Tool')

        # Initialize DataFrame placeholder
        self.df = None

        # Create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Functions Tab
        self.functions_tab = QWidget()
        self.tabs.addTab(self.functions_tab, "Functions")

        # Buttons for Functions Tab
        self.upload_csv_button = QPushButton("Upload CSV")
        self.upload_csv_button.clicked.connect(self.upload_csv)

        self.filter_df_button = QPushButton("Filter DataFrame")
        self.filter_df_button.clicked.connect(self.filter_dataframe)

        # Layout for Functions Tab
        functions_layout = QVBoxLayout()
        functions_layout.addWidget(self.upload_csv_button)
        functions_layout.addWidget(self.filter_df_button)
        self.functions_tab.setLayout(functions_layout)

        # Test Tab (Empty for now)
        self.test_tab = QWidget()
        self.tabs.addTab(self.test_tab, "Test")

    def upload_csv(self):
        selected_file_path = select_file()
        if selected_file_path:
            self.df = read_csv_with_logging(selected_file_path)
            print(f"DataFrame loaded with shape: {self.df.shape}")

    def filter_dataframe(self):
        if self.df is not None:
            selected_columns = select_columns(self.df)
            if selected_columns:
                self.df = self.df[selected_columns]
                print(f"DataFrame filtered with columns: {selected_columns}")
        else:
            print("Please upload a CSV file first.")


# Example usage
if __name__ == "__main__":
    # selected_file_path = select_file()
    # print(f"Selected File: {selected_file_path}")
    # df = read_csv_with_logging(selected_file_path)
    # selected_columns = select_columns(df)
    # print(f"Selected Columns: {selected_columns}")
    # # Filter the DataFrame based on selected columns
    # filtered_df = df[selected_columns]
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


# ToDo: Revert the column selector dialogue to previous version and see if it works.
