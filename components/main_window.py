import tkinter as tk
from typing import Callable, Tuple


class PasswordManagerUI:
    def __init__(
            self,
            main_frame: tk.Frame,
            title_font: Tuple[str, int, str],
            button_font: Tuple[str, int],
            button_color: str,
            button_text_color: str,
            background_color: str,
            show_add_password_frame: Callable,
            show_view_password_frame: Callable,
            show_edit_password_frame: Callable
    ):
        self.main_frame: tk.Frame = main_frame
        self.title_font: Tuple[str, int, str] = title_font
        self.button_font: Tuple[str, int] = button_font
        self.button_color: str = button_color
        self.button_text_color: str = button_text_color
        self.background_color: str = background_color

        # Create UI elements
        self.create_title_label()
        self.create_add_password_button(show_add_password_frame)
        self.create_view_password_button(show_view_password_frame)
        self.create_edit_password_button(show_edit_password_frame)

    def create_title_label(self) -> None:
        self.label: tk.Label = tk.Label(
            self.main_frame,
            text="Manage Passwords",
            font=self.title_font,
            fg="white",
            bg=self.background_color
        )
        self.label.pack(pady=20)

    def create_add_password_button(self, command: Callable) -> None:
        self.add_button: tk.Button = tk.Button(
            self.main_frame,
            text="Add Password",
            font=self.button_font,
            bg=self.button_color,
            fg=self.button_text_color,
            command=command,
        )
        self.add_button.pack(fill=tk.X, padx=20, pady=10)

    def create_view_password_button(self, command: Callable) -> None:
        self.view_button: tk.Button = tk.Button(
            self.main_frame,
            text="View Passwords",
            font=self.button_font,
            bg=self.button_color,
            fg=self.button_text_color,
            command=command
        )
        self.view_button.pack(fill=tk.X, padx=20, pady=10)

    def create_edit_password_button(self, command: Callable) -> None:
        self.edit_button: tk.Button = tk.Button(
            self.main_frame,
            text="Edit Password",
            font=self.button_font,
            bg=self.button_color,
            fg=self.button_text_color,
            command=command
        )
        self.edit_button.pack(fill=tk.X, padx=20, pady=10)

    def pack(self) -> None:
        self.main_frame.pack()

    def update_theme(self, button_color, button_text_color, background_color):
        self.main_frame.configure(bg=background_color)
        # for button in self.buttons:
        #     button.configure(bg=button_color, fg=button_text_color)