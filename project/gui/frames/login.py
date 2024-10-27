from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
import bcrypt

class LoginFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-size: 18px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #4C566A;
                border-radius: 5px;
                background-color: #3B4252;
                color: #D8DEE9;
            }
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #5E81AC;
                color: #ECEFF4;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)
        self.set_preferred_size()
        self.center_window()
        self.create_login_ui()
        
    def set_preferred_size(self):
        """Returns the preferred size of the frame."""
        self.screen_width = self.screen().size().width()
        self.screen_height = self.screen().size().height()
        self.window_width = 500
        self.window_height = 170
        
    def center_window(self):
        x_offset = int((self.screen_width - self.window_width) / 2)
        y_offset = int((self.screen_height - self.window_height) / 2)
        self.controller.setGeometry(x_offset, y_offset, self.window_width, self.window_height)
        
    def create_login_ui(self):
        layout = QVBoxLayout(self)
        
        self.password_label = QLabel("Password", self)
        self.password_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.password_label)
        
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)
        
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.on_login_button_click)
        layout.addWidget(self.login_button)
        
        self.error_label = QLabel("", self)  # Initialize the error label
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        
    def on_login_button_click(self):
        entered_password = self.password_entry.text()
        hashed_password = self.load_hashed_password()
        if bcrypt.checkpw(entered_password.encode(), hashed_password):
            self.password_entry.clear()
            hashed_password = None
            self.controller.show_frame("MainWindowFrame")
        else:
            self.error_label.setText("Senha inválida!")
            
    def load_hashed_password(self):
        return bcrypt.hashpw("senhacorreta".encode('utf-8'), bcrypt.gensalt(12))