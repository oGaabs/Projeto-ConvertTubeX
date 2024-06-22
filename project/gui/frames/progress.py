import tkinter as tk
from tkinter import ttk

class ProgressBarFrame(tk.Toplevel):
    def __init__(self, parent, download_location):
        super().__init__(parent)
        self.title("Progress")
        self.geometry("400x100")
        self.config(bg="black")
        self.download_location = download_location

        # Create a label with progress count and text
        self.progress_text = tk.StringVar()
        self.progress_label = tk.Label(self, textvariable=self.progress_text, bg="black", fg="white")
        self.progress_label.pack(pady=10)
        
        # Create the progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100
        self.update_progress(0)  # Initialize progress text


    def set_max_downloads(self, count):
        self.progress_bar["maximum"] = count
        self.update_progress(0)

    def reset_progress(self):
        self.progress_bar["value"] = 0
        self.update_progress_text(0, self.progress_bar["maximum"])  # Update text on reset

    def update_progress(self, value):
        self.progress_bar["value"] += value
        completed = self.progress_bar["value"]
        total = self.progress_bar["maximum"]
        self.update_progress_text(completed, total)

    def update_progress_text(self, completed, total):
        self.progress_text.set(f"Download progress Tasks: {completed}/{total}")
    