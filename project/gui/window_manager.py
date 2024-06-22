import tkinter as tk

from gui.frames.login import LoginFrame
from gui.frames.main_window import MainWindowFrame

class WindowManager:
    """Manages the display of different frames within the main application window."""

    def __init__(self, root):
        self.root = root
        self.container = tk.Frame(self.root)  # Create the container for frames
        
        self.frames = {}
        self.current_frame = None
        self.configure_root()
        self.initialize_frames()

        # Show the login frame initially
        self.show_frame("LoginFrame")
        
    def configure_root(self):
        """Configures the root window."""
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def initialize_frames(self):
        """Initializes all frames and stores them in a dictionary."""
        for F in (LoginFrame, MainWindowFrame):  # Add more frames here
            frame_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
    def show_frame(self, frame_name):
        """Shows the frame for the given frame name."""
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            
            if frame != self.current_frame:
                if self.current_frame:
                    self.current_frame.grid_remove()
                frame.grid()
                self.current_frame = frame
                self.adjust_window_size(frame)
                
            frame.tkraise()
    
    def adjust_window_size(self, frame):
        """Adjusts the root window size and position based on the frame's dimensions."""
        self.root.geometry(
            f"{frame.window_width}x{frame.window_height}+"
            f"{int(frame.screen_width/2 - frame.window_width/2)}+"
            f"{int(frame.screen_height/2 - frame.window_height/2)}"
        )
        
if __name__ == "__main__":
    window_manager = WindowManager(tk.Tk())
    window_manager.root.mainloop()
    