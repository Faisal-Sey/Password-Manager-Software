import tkinter as tk
from typing import Tuple
from components.add_password_window import AddPasswordFrame
from components.main_window import PasswordManagerUI
from components.view_password_window import ViewPasswordsFrame
from components.edit_password_window import EditPasswordFrame
from configuration.config import load_configurations
from helpers.common_functions import generate_secret_key


class PasswordManagerApp:
    def __init__(self, master: tk.Tk):
        self.master: tk.Tk = master
        self.master.title("Password Manager")

        self.main_frame: tk.Frame = tk.Frame(master)
        self.main_frame.pack()

        self.current_frame: tk.Frame = self.main_frame

        # Set fonts
        title_font: Tuple[str, int, str] = ("Helvetica", 24, "bold")
        button_font: Tuple[str, int] = ("Helvetica", 14)

        # Theme-related attributes
        self.is_dark_mode = True  # Default to dark mode
        self.dark_mode_colors = {
            "background": "#212121",  # Dark gray
            "button_bg": "#37474F",   # Blue gray
            "button_fg": "white",     # White
            "text_color": "white"
        }
        self.light_mode_colors = {
            "background": "#F0F0F0",  # Light gray
            "button_bg": "#E0E0E0",   # Light gray for buttons
            "button_fg": "black",     # Black text
            "text_color": "black"
        }

        # Initial mode setup (Dark mode)
        self.set_theme(self.dark_mode_colors)

        # Toggle button for dark mode / light mode
        self.toggle_mode_button = tk.Button(
            self.master,
            text="Switch to Light Mode",
            command=self.toggle_mode,
            font=("Helvetica", 12)
        )
        self.toggle_mode_button.pack(pady=10)

        # Initialize UI
        self.ui: PasswordManagerUI = PasswordManagerUI(
            main_frame=self.main_frame,
            title_font=title_font,
            button_font=button_font,
            button_color=self.dark_mode_colors["button_bg"],
            button_text_color=self.dark_mode_colors["button_fg"],
            background_color=self.dark_mode_colors["background"],
            show_add_password_frame=self.show_add_password_frame,
            show_view_password_frame=self.show_view_password_frame,
            show_edit_password_frame=self.show_edit_password_frame
        )
        self.ui.pack()

    def set_theme(self, theme_colors: dict):
        """Set theme for the application based on provided colors."""
        self.master.configure(bg=theme_colors["background"])
        self.main_frame.configure(bg=theme_colors["background"])

    def toggle_mode(self):
        """Switch between dark mode and light mode."""
        if self.is_dark_mode:
            # Switch to light mode
            self.set_theme(self.light_mode_colors)
            self.ui.update_theme(
                button_color=self.light_mode_colors["button_bg"],
                button_text_color=self.light_mode_colors["button_fg"],
                background_color=self.light_mode_colors["background"]
            )
            self.toggle_mode_button.config(text="Switch to Dark Mode")
        else:
            # Switch to dark mode
            self.set_theme(self.dark_mode_colors)
            self.ui.update_theme(
                button_color=self.dark_mode_colors["button_bg"],
                button_text_color=self.dark_mode_colors["button_fg"],
                background_color=self.dark_mode_colors["background"]
            )
            self.toggle_mode_button.config(text="Switch to Light Mode")

        # Toggle the mode state
        self.is_dark_mode = not self.is_dark_mode

    def show_frame(self, frame: tk.Frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame: tk.Frame = frame
        self.current_frame.pack()

    def show_main_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame: tk.Frame = self.main_frame
        self.current_frame.pack()

    def show_add_password_frame(self):
        add_password_frame = AddPasswordFrame(
            self.master,
            self.show_main_frame,
            self.dark_mode_colors if self.is_dark_mode else self.light_mode_colors
        )
        self.show_frame(add_password_frame)

    def show_view_password_frame(self):
        view_password_frame = ViewPasswordsFrame(
            self.master,
            self.show_main_frame,
            self.show_edit_password_frame,
            self.dark_mode_colors if self.is_dark_mode else self.light_mode_colors
        )
        self.show_frame(view_password_frame)

    def show_edit_password_frame(self):
        edit_password_frame = EditPasswordFrame(
            self.master,
            self.show_main_frame,
            self.dark_mode_colors if self.is_dark_mode else self.light_mode_colors
        )
        self.show_frame(edit_password_frame)


root = tk.Tk()
root.geometry("1000x700")
load_configurations()
app = PasswordManagerApp(root)
root.mainloop()
