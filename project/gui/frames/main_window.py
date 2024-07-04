import sys
import threading
import tkinter as tk
from tkinter import END, filedialog, font, messagebox
from time import perf_counter

# Local application imports
sys.path.append('../../services')
from services.download_service import YoutubeConverter
from services.conversion_service import ConversionService
from gui.frames.progress import ProgressBarFrame

class MainWindowFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.download_service = None
        self.progress_bar_frame = None
        self.configure_gui()
        
    def configure_gui(self):
        self.config(bg="black")
        self.setup_widgets()
        self.bind_events()
        self.set_window_size()

    def setup_widgets(self):
        self.title_label = tk.Label(self, text="ConvertTubeX", bg="black", fg="white",
                                    font=font.Font(family='Helvetica', size=36, weight="bold"))
        self.title_label.grid(row=0, column=1, columnspan=2)

        self.subtitle_label = tk.Label(self, text="Desenvolvido por Gabriel S.", bg="black", fg="white",
                                       font=font.Font(family='Helvetica', size=12))
        self.subtitle_label.grid(row=1, column=1, columnspan=2, pady=10)

        tk.Label(self, text="Salvar em:", bg="black", fg="white",
                 font=font.Font(family='Helvetica', size=12)).grid(row=2, column=2, padx=20, pady=10, sticky="e")
        self.download_location_var = tk.StringVar()
        tk.Button(self, text="Selecionar Local", command=self.select_download_location).grid(row=2, column=3, padx=10, pady=10)

        conversion_options = ["MP3", "MP4"]
        self.conversion_type_var = tk.StringVar()
        self.conversion_type_var.set(conversion_options[0])
        tk.Label(self, text="Tipo:", bg="black", fg="white",
                 font=font.Font(family='Helvetica', size=12)).grid(row=2, column=0, padx=20, pady=10, sticky="e")
        tk.OptionMenu(self, self.conversion_type_var, *conversion_options).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Link:", bg="black", fg="white",
                 font=font.Font(family='Helvetica', size=12)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.link_entry = tk.Entry(self, bg="white", fg="black", font=font.Font(family='Helvetica', size=12))
        self.link_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Button(self, text="DOWNLOAD", bg="red", fg="white",
                  font=font.Font(family='Helvetica', size=12, weight="bold"),
                  command=self.btn_start_download).grid(row=3, column=3, padx=20, pady=10)

    def bind_events(self):
        self.link_entry.bind("<Return>", lambda event: self.start_download())
        
    def set_window_size(self):
        self.screen_width = self.controller.root.winfo_screenwidth()
        self.screen_height = self.controller.root.winfo_screenheight()
        self.window_width = 600
        self.window_height = 250
      
        x_offset = int((self.screen_width - self.window_width) / 2)
        y_offset = int((self.screen_height - self.window_height) / 2)
        self.controller.root.geometry(f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

       

    def select_download_location(self):
        """Opens a file dialog to select the download location."""
        download_location = filedialog.askdirectory()
        if download_location:
            self.download_location_var.set(download_location)

    def btn_start_download(self):
        """Handles the confirmation and download process."""
        links = self.link_entry.get()
        conversion_type = self.conversion_type_var.get()
        download_location = self.download_location_var.get()

        if not links:
            messagebox.showerror("Erro", "Insira pelo menos um link.")
            return

        if not download_location:
            messagebox.showerror("Erro", "Selecione um local de download.")
            return

        links = links.strip('\t\n\r').replace(' ', '').split(',')

        self.download_service = YoutubeConverter(download_location, conversion_type)
        try:
            self.download_service.validate_links(links)
            links = self.download_service.convert_playlists_to_link(links)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        
        # Iniciar thread para download e conversão
        thread = threading.Thread(target=self.download_and_convert_videos, args=(links, conversion_type, download_location))
        thread.start()
        
    def download_and_convert_videos(self, links, conversion_type, download_location):     
        self.spawn_progress_bar(download_location)
        self.progress_bar_frame.set_max_downloads(len(links))
        
        t1_start = perf_counter() 
        self.download_service.download_videos(links, self.update_progress)
        t1_stop = perf_counter()
        
        if conversion_type == 'MP4':
            messagebox.showinfo('FINISHED', f'Conversão concluída! Em: {(t1_stop-t1_start):.2f} segs')
        elif conversion_type == 'MP3':
            self.reset_progress()
            
            t1_start = perf_counter() 
            conversion_service = ConversionService()
            conversion_service.convert_mp4_to_mp3(self.download_service.get_downloaded_mp4s(), self.update_progress)
            t1_stop = perf_counter()
                
            messagebox.showinfo('FINISHED', f'Vídeos convertidos para MP3!  Em: {(t1_stop-t1_start):.2f} segs' )
            self.destroy_progress_bar()
    
    # ProgressBar
    def reset_progress(self):
        if self.progress_bar_frame:
                self.progress_bar_frame.reset_progress()
                
    def update_progress(self, value):
        if self.progress_bar_frame:
            self.progress_bar_frame.update_progress(value)  
              
    def spawn_progress_bar(self, download_location):
        if not self.progress_bar_frame:
            self.progress_bar_frame = ProgressBarFrame(self, download_location)
            self.progress_bar_frame.protocol("WM_DELETE_WINDOW", self.destroy_progress_bar)
            self.progress_bar_frame.lift()
            
    def destroy_progress_bar(self):
        if self.progress_bar_frame:
            self.progress_bar_frame.destroy()
            self.progress_bar_frame = None
