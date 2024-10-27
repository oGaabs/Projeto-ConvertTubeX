from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QMessageBox
from PySide6.QtCore import Qt, Signal, Slot, QElapsedTimer

class ProgressBarFrame(QDialog):
    def __init__(self, download_location):
        super().__init__()
        self.setWindowTitle("Progress")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-size: 18px;
            }
            QProgressBar {
                border: 1px solid #4C566A;
                border-radius: 5px;
                background-color: #3B4252;
                color: #D8DEE9;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5E81AC;
            }
        """)
        self.download_location = download_location
        self.timer = QElapsedTimer()
        self.timer.start()
        self.timerall = QElapsedTimer()
        self.timerall.start()

        # Create a label with progress count and text
        self.progress_text = QLabel(self)
        self.progress_text.setAlignment(Qt.AlignCenter)

        # Create a label for estimated time remaining
        self.eta_label = QLabel("Estimated Time Remaining: Calculating...", self)
        self.eta_label.setAlignment(Qt.AlignCenter)

        # Create the progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.setFixedWidth(300)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_text)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.eta_label)
        self.setLayout(layout)

        self.update_progress(0)  # Initialize progress text

    def set_max_downloads(self, count):
        self.progress_bar.setRange(0, count)
        self.update_progress(0)

    def reset_progress(self):
        self.progress_bar.setValue(0)
        self.timer.restart()
        self.update_progress_text(0, self.progress_bar.maximum())  # Update text on reset

    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(self.progress_bar.value() + value)
        self.update_progress_text(self.progress_bar.value(), self.progress_bar.maximum())
        self.update_eta()

    def update_progress_text(self, current, maximum):
        self.progress_text.setText(f"Progress: {current}/{maximum}")

    def update_eta(self):
        elapsed_time = self.timer.elapsed() / 1000  # Convert milliseconds to seconds
        progress = self.progress_bar.value()
        if progress > 0:
            total_time = (elapsed_time / progress) * self.progress_bar.maximum()
            remaining_time = total_time - elapsed_time
            self.eta_label.setText(f"Estimated Time Remaining: {self.format_time(remaining_time)}")

    def format_time(self, seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes}m {seconds}s"