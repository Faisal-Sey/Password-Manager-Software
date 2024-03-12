import tkinter as tk
from typing import Tuple

from components.add_password_window import AddPasswordFrame
from components.main_window import PasswordManagerUI
from components.view_password_window import ViewPasswordsFrame
from components.edit_password_window import EditPasswordFrame
from configuration.config import load_configurations


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

        # Set colors
        background_color: str = "#212121"  # Dark gray
        button_color: str = "#37474F"       # Blue gray
        button_text_color: str = "white"    # White

        # Set background color
        # self.master.configure(bg=background_color)

        self.ui: PasswordManagerUI = PasswordManagerUI(
            main_frame=self.main_frame,
            title_font=title_font,
            button_font=button_font,
            button_color=button_color,
            button_text_color=button_text_color,
            background_color=background_color,
            show_add_password_frame=self.show_add_password_frame,
            show_view_password_frame=self.show_view_password_frame,
            show_edit_password_frame=self.show_edit_password_frame
        )

        self.ui.pack()

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
        add_password_frame = AddPasswordFrame(self.master, self.show_main_frame)
        self.show_frame(add_password_frame)

    def show_view_password_frame(self):
        view_password_frame = ViewPasswordsFrame(
            self.master,
            self.show_main_frame,
            self.show_edit_password_frame
        )
        self.show_frame(view_password_frame)

    def show_edit_password_frame(self):
        edit_password_frame = EditPasswordFrame(self.master, self.show_main_frame)
        self.show_frame(edit_password_frame)


root = tk.Tk()
root.geometry("1000x700")
load_configurations()
app = PasswordManagerApp(root)
root.mainloop()
