import sys
import requests
from configparser import ConfigParser
from PyQt6.QtWidgets import QApplication,\
    QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QSpinBox
from PyQt6.QtCore import QTimer  # Import QTimer
from config import create_or_load_ini_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window/central widget stuff
        self.setWindowTitle("PlayTrade")
        self.resize(500, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Config file
        self.config = ConfigParser()
        self.config_file_funct = create_or_load_ini_file()

        self.config.read('config.ini')

        self.ui_widget()
        self.loop_running = False  # Initialize loop_running

    def ui_widget(self):
        # Create a layout for the central widget
        self.layout = QVBoxLayout(self.central_widget)

        # Create a form layout for username and server name
        self.form_layout = QFormLayout()

        # Create input boxes for username and server name
        self.user_token = QLineEdit()
        self.server_id = QLineEdit()
        self.time_input = QSpinBox()

        # Default value
        self.user_token.setText(self.config.get('Settings', 'token'))
        self.server_id.setText(self.config.get('Settings', 'serverid'))
        self.time_input.setMinimum(2)

        # Add labels and line edits to the form layout
        self.form_layout.addRow("Discord Token:", self.user_token)
        self.form_layout.addRow("Channel Id:", self.server_id)
        self.form_layout.addRow("Repeat every (seconds):", self.time_input)

        # Create a large input box
        self.message_box = QTextEdit()

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.toggle_loop)

        # Save token and server
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)

        # Add the form layout and the input box to the main layout
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.message_box)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.save_button)


    def save_config(self):
        """
        Save the current input
        """
        self.config['Settings']['token'] = self.user_token.text()
        self.config['Settings']['serverid'] = self.server_id.text()

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def toggle_loop(self):
        """
        Toggle the loop for starting
        """
        if not self.loop_running:
            # Start the loop
            self.start_button.setText("Stop")  # Update the button label
            self.loop_running = True
            self.run_loop()
        else:
            # Stop the loop
            self.start_button.setText("Start")  # Update the button label
            self.loop_running = False

    def run_loop(self):
        """
        Part of the loop and responsible for looping
        """
        seconds = int(self.time_input.text())
        milliseconds = seconds * 1000  # Convert seconds to milliseconds

        payload = {
            "content": self.message_box.toPlainText()
        }

        header = {
            "authorization": self.user_token.text()
        }

        # Your loop logic goes here

        if self.loop_running:
            requests.post(f"https://discord.com/api/v9/channels/{self.server_id.text()}/messages", data=payload,
                          headers=header)

            QTimer.singleShot(milliseconds, self.run_loop)  # Continue the loop after 1 second


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
