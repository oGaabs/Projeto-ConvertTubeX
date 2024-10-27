import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox
from PySide6.QtCore import Qt, QThread, Signal

# Local application imports
sys.path.append('../../services')
from services.download_service import YoutubeConverter
from services.conversion_service import ConversionService
from gui.frames.progress import ProgressBarFrame

class DownloadThread(QThread):
    def __init__(self, download_service, links, update_progress):
        super().__init__()
        self.download_service = download_service
        self.links = links
        self.update_progress = update_progress

    def run(self):
        self.download_service.download_videos(self.links, self.update_progress)

class ConversionThread(QThread):
    def __init__(self, conversion_service, video_files, conversion_type, update_progress):
        super().__init__()
        self.conversion_service = conversion_service
        self.video_files = video_files
        self.conversion_type = conversion_type
        self.update_progress = update_progress
        self._is_running = True

    def run(self):
        self.conversion_service.convert_mp4_to_mp3(self.video_files, self.update_progress)
    

class MainWindowFrame(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.download_service = None
        self.conversion_service = None
        self.progress_bar_frame = None
        self.configure_gui()
        
    def configure_gui(self):
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
            QComboBox {
                padding: 10px;
                border: 1px solid #4C566A;
                border-radius: 5px;
                background-color: #3B4252;
                color: #D8DEE9;
            }
        """)
        self.setup_widgets()
        self.set_window_size()
        
    def setup_widgets(self):
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel("ConvertTubeX", self)
        self.title_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        
        self.subtitle_label = QLabel("Desenvolvido por Gabriel S.", self)
        self.subtitle_label.setStyleSheet("font-size: 12px;")
        layout.addWidget(self.subtitle_label, alignment=Qt.AlignCenter)
        
        self.download_location_var = ""
        self.select_location_button = QPushButton("Selecionar Local", self)
        self.select_location_button.clicked.connect(self.select_download_location)
        layout.addWidget(self.select_location_button, alignment=Qt.AlignCenter)
        
        self.conversion_type_var = QComboBox(self)
        self.conversion_type_var.addItems(["MP3", "MP4"])
        layout.addWidget(self.conversion_type_var, alignment=Qt.AlignCenter)
        
        self.link_entry = QLineEdit(self)
        self.link_entry.setPlaceholderText("Link")
        layout.addWidget(self.link_entry, alignment=Qt.AlignCenter)
        
        self.download_button = QPushButton("DOWNLOAD", self)
        self.download_button.setStyleSheet("background-color: #BF616A;")
        self.download_button.clicked.connect(self.btn_start_download)
        layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
    def set_window_size(self):
        self.screen_width = self.screen().size().width()
        self.screen_height = self.screen().size().height()
        self.window_width = 600
        self.window_height = 250
      
        x_offset = int((self.screen_width - self.window_width) / 2)
        y_offset = int((self.screen_height - self.window_height) / 2)
        self.controller.setGeometry(x_offset, y_offset, self.window_width, self.window_height)
    
    def select_download_location(self):
        """Opens a file dialog to select the download location."""
        download_location = QFileDialog.getExistingDirectory(self, "Select Download Location")
        if download_location:
            self.download_location_var = download_location
            
    def btn_start_download(self):
        """Handles the confirmation and download process."""
        links = self.link_entry.text()
        conversion_type = self.conversion_type_var.currentText()
        download_location = self.download_location_var
        if not links:
            QMessageBox.critical(self, "Erro", "Insira pelo menos um link.")
            return
        if not download_location:
            QMessageBox.critical(self, "Erro", "Selecione um local de download.")
            return
        links = links.strip('\t\n\r').replace(' ', '').split(',')
        self.download_service = YoutubeConverter(download_location, conversion_type)
        try:
            self.download_service.validate_links(links)
            links = self.download_service.convert_playlists_to_link(links)
        except ValueError as e:
            QMessageBox.critical(self, "Erro", str(e))
            return
        self.conversion_service = ConversionService()
        
        self.spawn_progress_bar(download_location)
        self.progress_bar_frame.set_max_downloads(len(links))
        
        # Iniciar thread para download e conversão
        self.download_thread = DownloadThread(self.download_service, links, self.update_progress)
        self.download_thread.finished.connect(self.start_conversion)  # Connect to start conversion after download
        self.download_thread.start()
        
    def start_conversion(self):
        """Starts the conversion process after download is complete."""
        self.progress_bar_frame.reset_progress() 
        
        conversion_type = self.conversion_type_var.currentText()
        if conversion_type == "MP4":
            return self.destroy_progress_bar()
        video_files = self.download_service.get_downloaded_mp4s()
        
        self.conversion_thread = ConversionThread(self.conversion_service, video_files, conversion_type, self.update_progress)
        self.conversion_thread.finished.connect(self.destroy_progress_bar)  
        self.conversion_thread.start()

    def update_progress(self, value):
        if self.progress_bar_frame:
            self.progress_bar_frame.update_progress(value)
            
    def spawn_progress_bar(self, download_location):
        if not self.progress_bar_frame:
            self.progress_bar_frame = ProgressBarFrame(download_location)
            self.progress_bar_frame.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.progress_bar_frame.show()

    def destroy_progress_bar(self):
        if self.progress_bar_frame:
            self.progress_bar_frame.accept()
            
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Download and Conversion Complete")
            msg_box.setText(f"Download e conversão concluídos em {self.progress_bar_frame.format_time(self.progress_bar_frame.timerall.elapsed() / 100)}")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
            
            self.progress_bar_frame = None