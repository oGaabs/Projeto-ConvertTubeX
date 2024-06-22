import tkinter as tk
import bcrypt

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Use super() for proper inheritance
        self.controller = controller

        # Set up the main window
        self.controller.root.title("Login - ConvertTubeX")
        self.config(bg="black")  # Explicitly set background color to black

        self.set_preferred_size()
        self.center_window()

        # Create the login UI elements
        self.create_login_ui()
        
    def set_preferred_size(self):
        """Returns the preferred size of the frame."""
        self.screen_width = self.controller.root.winfo_screenwidth()
        self.screen_height = self.controller.root.winfo_screenheight()

        # Define window size and position (40% width, 30% height, centered)
        self.window_width = int(self.screen_width * 0.3)
        self.window_height = int(self.screen_height * 0.2)

    def center_window(self):
        self.controller.root.geometry(
            f"{self.window_width}x{self.window_height}+{int(self.screen_width/2 - self.window_width/2)}+{int(self.screen_height/2 - self.window_height/2)}"
        )

    def create_login_ui(self):
        # Label for password (centered)
        self.password_label = tk.Label(self, text="Password:", fg="white", bg="black")
        self.password_label.pack(anchor="center", padx=5, pady=10)

        self.password_entry = tk.Entry(self, show="*", bg="black", fg="white")
        self.password_entry.pack(anchor="center", padx=5, pady=10)

        login_btn = tk.Button(
            self, text="Entrar", command=self.login, fg="white", bg="red"
        )
        login_btn.pack(anchor="center", padx=10, pady=10)

        self.error_label = tk.Label(self, text="", fg="red", bg="black")
        self.error_label.pack(anchor="center", padx=10, pady=10)

    def login(self):
        entered_password = self.password_entry.get()
        correct_password = "senhacorreta"
        
        if entered_password == correct_password:            
            self.password_entry.delete(0, tk.END)  # Clear password entry
            correct_password = ""
            
            self.controller.show_frame("MainWindowFrame")
        else:
            self.error_label.config(text="Senha inválida!")
            
    def login(self):
        entered_password = self.password_entry.get()

        # Load hashed password from a secure location (e.g., database)
        hashed_password = self.load_hashed_password()

        if bcrypt.checkpw(entered_password.encode(), hashed_password):
            self.password_entry.delete(0, tk.END)
            hashed_password = None  # Clear sensitive data
            
            self.controller.show_frame("MainWindowFrame")
        else:
            self.error_label.config(text="Senha inválida!")

    def load_hashed_password(self):
        return bcrypt.hashpw("senhacorreta".encode('utf-8'), bcrypt.gensalt(12))
