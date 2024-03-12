import tkinter as tk
from tkinter import messagebox
from typing import Callable, List, Tuple, Dict, Any

from pip._internal.utils import misc

from helpers.common_functions import map_data_to_dict, decrypt_password
from helpers.data import MODEL_KEYS
from helpers.logger import logger
from services.queries import read_all_data
from store.app_context import app_context
from typings.configuration_types import CursorType, ConnectionType


class PasswordEntry(tk.Frame):
    def __init__(
            self,
            master: misc,
            title: str,
            username: str,
            password: str,
            website: str,
            description: str,
            is_active: bool,
            is_favorite: bool,
            show_edit_password_frame: Callable
    ):
        super().__init__(master, bg="white", padx=10, pady=5)

        # Title label
        self.title_label: tk.Label = tk.Label(self, text=title, font=("Arial", 12), bg="white")
        self.title_label.grid(row=0, column=0, sticky="w")

        # Username label
        self.username_label: tk.Label = tk.Label(self, text=username, font=("Arial", 10), bg="white", fg="gray")
        self.username_label.grid(row=1, column=0, sticky="w")

        # Password label (hidden by default)
        self.password_label: tk.Label = tk.Label(self, text="****", font=("Arial", 10), bg="white", fg="gray")
        self.password_label.grid(row=2, column=0, sticky="w")

        # Reveal button to show password
        self.reveal_button: tk.Button = tk.Button(self, text="Reveal", command=self.reveal_password)
        self.reveal_button.grid(row=2, column=1, padx=(10, 0))

        # View, Edit, Delete buttons
        self.view_button: tk.Button = tk.Button(self, text="Copy", command=self.copy_password)
        self.view_button.grid(row=2, column=2, pady=5)

        self.edit_button: tk.Button = tk.Button(self, text="Edit", command=self.edit_password)
        self.edit_button.grid(row=2, column=3, pady=5)

        self.delete_button: tk.Button = tk.Button(self, text="Delete", command=self.delete_password)
        self.delete_button.grid(row=2, column=4, pady=5)

        # Store actual password for revealing
        self.password: str = password
        self.description: str = description
        self.website: str = website
        self.is_active: bool = is_active
        self.is_favorite: bool = is_favorite
        self.show_edit_password_frame = show_edit_password_frame

    def reveal_password(self) -> None:
        if self.password_label.cget("text") == "****":
            self.password_label.config(text=self.password)
            self.reveal_button.config(text="Hide")
        else:
            self.password_label.config(text="****")
            self.reveal_button.config(text="Reveal")

    def copy_password(self) -> None:
        self.master.clipboard_clear()
        self.master.clipboard_append(self.password)
        messagebox.showinfo("Password", "Password copied successfully")

    def edit_password(self) -> None:
        current_data = {
            "title": self.title_label.cget("text"),
            "username": self.username_label.cget("text"),
            "password": self.password,
            "description": self.description,
            "website": self.website,
            "is_active": self.is_active,
            "is_favorite": self.is_favorite
        }
        app_context.set_config("current_password_data", current_data)
        self.show_edit_password_frame()

    def delete_password(self) -> None:
        # Implement delete functionality
        pass


class ViewPasswordsFrame(tk.Frame):
    def __init__(
            self,
            master: misc,
            show_main_frame: Callable,
            show_edit_password_frame: Callable
    ):
        super().__init__(master)
        self.master: tk.Tk = master
        self.master.title("View Passwords")
        self.cursor: CursorType = app_context.get_config("db_cursor")
        self.conn: ConnectionType = app_context.get_config("db_connection")
        self.show_edit_password_frame = show_edit_password_frame

        # Create a Canvas widget to hold the scrollable frame
        self.canvas = tk.Canvas(self, width=1000, height=700)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a scrollbar and associate it with the Canvas
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the Canvas to hold the widgets
        frame = tk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        # Bind the scrollbar to the frame for scrolling effect
        frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Configure grid inside the frame
        frame.grid_rowconfigure(0, weight=0)  # Title row
        frame.grid_rowconfigure(1, weight=1)  # PasswordEntry rows
        frame.grid_columnconfigure(0, weight=1)

        # Create UI elements
        self.create_title_label(frame)
        self.create_password_list(frame)
        self.create_buttons(frame, show_main_frame)


    def create_title_label(self, frame: tk.Frame) -> None:
        title_label: tk.Label = tk.Label(
            frame,
            text="Your Passwords",
            font=("Helvetica", 18, "bold"),
            bg="lightgrey",
            padx=10,
            pady=10
        )
        title_label.grid(row=0, column=0, sticky="ew")

    def create_password_list(self, frame: tk.Frame) -> None:
        try:
            passwords: List[Tuple] = read_all_data(
                self.cursor,
                "passwords",
                '*',
                "created_on",
            )
            # Display passwords in the UI
            for i, password_values in enumerate(passwords, start=5):
                password: Dict[str, Any] = map_data_to_dict(MODEL_KEYS, list(password_values))
                title: str = password.get('title')
                username: str = password.get('username')
                actual_password: str = decrypt_password(password.get('password')).decode('utf-8')
                website: str = password.get('website')
                description: str = password.get('description')
                is_active: bool = password.get("is_active")
                is_favorite: bool = password.get("is_favorite")

                # Create PasswordEntry for each password
                password_entry: PasswordEntry = PasswordEntry(
                    frame,
                    title,
                    username,
                    actual_password,
                    website,
                    description,
                    is_active,
                    is_favorite,
                    self.show_edit_password_frame
                )

                # Arrange PasswordEntry side-by-side
                row = (i - 1) // 2  # Calculate row index based on current index
                col = (i - 1) % 2  # Calculate column index based on current index
                password_entry.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching passwords: {e}")
            logger(
                "access",
                "error",
                f"Error fetching passwords: {e}",
            )

    def create_buttons(self, frame: tk.Frame, show_main_frame: Callable) -> None:
        back_button: tk.Button = tk.Button(
            frame,
            text="Back",
            font=("Helvetica", 12),
            bg="lightgrey",
            command=show_main_frame
        )
        back_button.grid(row=99, column=0, pady=20, sticky="ew")
