from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QMainWindow
from gui.frames.main_window import MainWindowFrame
from gui.frames.login import LoginFrame

class WindowManager(QMainWindow):
    """Manages the display of different frames within the main application window."""
    def __init__(self):
        super().__init__()
        self.container = QStackedWidget(self)  # Create the container for frames
        
        self.frames = {}
        self.current_frame = None
        self.configure_root()
        self.initialize_frames()
        # Show the login frame initially
        self.show_frame("LoginFrame")
        
    def configure_root(self):
        """Configures the root window."""
        self.setWindowTitle("ConvertTubeX")
        layout = QVBoxLayout()
        layout.addWidget(self.container)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    def initialize_frames(self):
        """Initializes all frames and stores them in a dictionary."""
        for F in (LoginFrame, MainWindowFrame):  # Add more frames here
            frame_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[frame_name] = frame
            self.container.addWidget(frame)
        
    def show_frame(self, frame_name):
        """Shows the frame for the given frame name."""
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            self.container.setCurrentWidget(frame)
            if frame_name == "LoginFrame":
                self.setWindowTitle("Login - ConvertTubeX")
            elif frame_name == "MainWindowFrame":
                self.setWindowTitle("Main Window - ConvertTubeX")