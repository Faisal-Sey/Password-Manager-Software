import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import Callable

from pip._internal.utils import misc

from helpers.common_functions import encrypt_password
from services.queries import create_data
from store.app_context import app_context


class EditPasswordFrame(tk.Frame):
    def __init__(self, master: misc, show_main_frame: Callable):
        super().__init__(master)
        self.master: tk.Tk = master
        self.master.title("Edit Password")
        self.current_password_data = app_context.get_config("current_password_data")

        self.configure(bg="#f0f0f0")  # Background color

        # Create frames for grouping
        left_frame = tk.Frame(self, bg="#f0f0f0")
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, bg="#f0f0f0")
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Labels and Entry widgets
        left_fields = [
            ("Title:", tk.Entry),
            ("Username:", tk.Entry),
            ("Password:", tk.Entry),
            ("Website:", tk.Entry),
        ]

        right_fields = [
            ("Description:", tk.Text),
            ("Is Active:", tk.Checkbutton),
            ("Is Favorite:", tk.Checkbutton)
        ]

        self.entry_widgets = {}
        self.checkbox_vars = {}

        for i, (label_text, widget_type) in enumerate(left_fields):
            label = tk.Label(left_frame, text=label_text, font=("Arial", 12), bg="#f0f0f0")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            widget = widget_type(left_frame, font=("Arial", 12), bg="white")
            if label_text == "Password:":
                password_entry = widget_type(left_frame, font=("Arial", 12), bg="white", show="*")
                password_entry.grid(row=i, column=1, padx=5, pady=5)
                show_password_button = tk.Button(
                    left_frame,
                    text="Show",
                    command=lambda entry=password_entry: self.toggle_password_visibility(entry)
                )
                show_password_button.grid(row=i, column=2, padx=5, pady=5)
                self.entry_widgets["password"] = password_entry
            else:
                widget.grid(row=i, column=1, padx=5, pady=5)
                self.entry_widgets[label_text.lower().strip(":").replace(" ", "_")] = widget

        for i, (label_text, widget_type) in enumerate(right_fields):
            label = tk.Label(right_frame, text=label_text, font=("Arial", 12), bg="#f0f0f0")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            if widget_type == tk.Text:
                widget = widget_type(right_frame, height=5, width=30)
                widget.grid(row=i, column=1, padx=5, pady=5)
                self.entry_widgets[label_text.lower().strip(":").replace(" ", "_")] = widget
            elif widget_type == tk.Checkbutton:
                widget_var = tk.BooleanVar()
                widget = tk.Checkbutton(right_frame, variable=widget_var, onvalue=True, offvalue=False)
                self.checkbox_vars[label_text.lower().strip(":").replace(" ", "_")] = widget_var
                widget.grid(row=i, column=1, padx=5, pady=5, sticky="w")
                self.entry_widgets[label_text.lower().strip(":").replace(" ", "_")] = widget

        # Buttons
        self.add_button = tk.Button(self, text="Add", font=("Arial", 12), bg="blue", fg="white",
                                    command=self.add_password)
        self.add_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(self, text="Back", font=("Arial", 12),
                                    command=self.go_to_main_frame)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=14)

        # Function to navigate back to the main frame
        self.show_main_frame = show_main_frame

        self.update_ui_for_edit(self.current_password_data)

    def update_ui_for_edit(self, password_data: dict):
        # Set values from database for fields
        print(self.entry_widgets)
        for field, value in password_data.items():
            print(f"Field: {field}, Value: {value}")
            if field == "is_active" or field == "is_favorite":
                self.checkbox_vars[field].set(value)
            elif field == "password":
                self.entry_widgets[field].delete(0, tk.END)
                self.entry_widgets[field].insert(0, value)
            else:
                self.entry_widgets[field].delete("1.0", tk.END)
                self.entry_widgets[field].insert("1.0", value)

        # Update button text
        self.add_button.config(text="Edit", command=self.add_password)

    def go_to_main_frame(self):
        self.show_main_frame()

    def add_password(self):
        # Retrieve values from entry widgets
        username: str = self.entry_widgets["username"].get()
        title = self.entry_widgets["title"].get()
        website = self.entry_widgets["website"].get()
        password = self.entry_widgets["password"].get()
        description = self.entry_widgets["description"].get("1.0", tk.END).strip()
        is_active = self.checkbox_vars["is_active"].get()
        is_favorite = self.checkbox_vars["is_favorite"].get()

        encrypted_password: bytes = encrypt_password(password)

        # Add the password to the database
        data = {
            "title": title,
            "username": username,
            "website": website,
            "password": encrypted_password,
            "description": description,
            "is_active": is_active,
            "is_favorite": is_favorite,
            "created_on": datetime.now(),
            "updated_on": None,
        }

        cursor = app_context.get_config("db_cursor")
        conn = app_context.get_config("db_connection")

        create_data(
            cursor,
            conn,
            "passwords",
            data
        )

        # Display success message
        messagebox.showinfo("Success", "Password added successfully")

        # Navigate back to main frame
        self.show_main_frame()

    def toggle_password_visibility(self, entry):
        current_showing = entry.cget("show")
        if current_showing == "*":
            entry.config(show="")
        else:
            entry.config(show="*")
