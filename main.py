import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class PasswordSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Saver")
        self.root.configure(bg="#f0f0f0")
        
        self.header_label = tk.Label(root, text="Password Saver", font=("Helvetica", 16), bg="#0077FF", fg="white")
        self.header_label.grid(row=0, columnspan=4, sticky="ew")
        
        self.form_frame = tk.Frame(root, bg="#f0f0f0")
        self.form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.website_label = tk.Label(self.form_frame, text="Website:", bg="#f0f0f0")
        self.website_label.grid(row=0, column=0, sticky="w")
        self.website_entry = tk.Entry(self.form_frame)
        self.website_entry.grid(row=0, column=1, padx=5, pady=5)

        self.username_label = tk.Label(self.form_frame, text="Username:", bg="#f0f0f0")
        self.username_label.grid(row=1, column=0, sticky="w")
        self.username_entry = tk.Entry(self.form_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.form_frame, text="Password:", bg="#f0f0f0")
        self.password_label.grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self.form_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Watch Password Checkbox
        self.watch_password_var = tk.BooleanVar()
        self.watch_password_checkbox = tk.Checkbutton(root, text="Watch Password", variable=self.watch_password_var, bg="#f0f0f0")
        self.watch_password_checkbox.grid(row=3, columnspan=2, padx=20, pady=(0, 10), sticky="w")

        self.password_entry.bind("<KeyRelease>", self.watch_password)

        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.grid(row=1, column=1, padx=20, pady=10, sticky="e")

        self.save_button = tk.Button(self.button_frame, text="Save Password", command=self.save_password, bg="#0077FF", fg="white")
        self.save_button.pack(side="left", padx=5)

        self.modify_button = tk.Button(self.button_frame, text="Modify", command=self.modify_password, bg="#0077FF", fg="white")
        self.modify_button.pack(side="left", padx=5)

        # Update Button
        self.update_button = tk.Button(self.button_frame, text="Update", command=self.update_password, bg="#0077FF", fg="white", state="disabled")
        self.update_button.pack(side="left", padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove", command=self.remove_password, bg="#FF4444", fg="white")
        self.remove_button.pack(side="left", padx=5)

        self.clear_all_button = tk.Button(self.button_frame, text="Clear All", command=self.clear_all_passwords, bg="#FF4444", fg="white")
        self.clear_all_button.pack(side="left", padx=5)

        self.password_list = tk.Listbox(root, width=50, height=10, bg="white")
        self.password_list.grid(row=2, columnspan=4, padx=20, pady=(0, 10), sticky="ew")

        # Selected password index and details
        self.selected_password_index = None
        self.selected_password_details = None

        self.history_button = tk.Button(self.button_frame, text="Historique", command=self.show_history, bg="#FFBB33", fg="white")
        self.history_button.pack(side="left", padx=5)
        
        self.history_entries = []
        self.recent_changes = []

        self.setup_responsive_layout()

        self.display_saved_passwords()

    def setup_responsive_layout(self):
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)
            
    def save_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            if self.check_existing_credentials(website, username, password):
                messagebox.showinfo("Credentials Already Exist", "You already have credentials for this website with the same username and password.")
            else:
                with open("passwords.txt", "a") as f:
                    f.write(f"Website: {website}, Username: {username}, Password: {password}\n")

                # Add history entry
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.history_entries.append(f"{timestamp}: Saved - Website: {website}, Username: {username}, Password: {password}")

                self.website_entry.delete(0, "end")
                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")

                self.display_saved_passwords()
        else:
            messagebox.showerror("Error", "Please enter all fields")

    def check_existing_credentials(self, website, username, password):
        try:
            with open("passwords.txt", "r") as f:
                passwords = f.readlines()
                for password in passwords:
                    if f"Website: {website}" in password:
                        saved_username = self.extract_field_value(password, "Username")
                        saved_password = self.extract_field_value(password, "Password")
                        if saved_username == username and saved_password == password:
                            return True
                return False
        except FileNotFoundError:
            return False

    def extract_field_value(self, text, field_name):
        start_index = text.find(field_name + ": ") + len(field_name) + 2
        end_index = text.find(", ", start_index)
        return text[start_index:end_index]


    def display_saved_passwords(self):
        self.password_list.delete(0, "end")

        try:
            with open("passwords.txt", "r") as f:
                passwords = f.readlines()
                for password in passwords:
                    self.password_list.insert("end", password.strip())
        except FileNotFoundError:
            pass

    def watch_password(self, event):
        if self.watch_password_var.get():
            password = self.password_entry.get()
            self.password_entry.config(show="")
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, password)
        else:
            self.password_entry.config(show="*")

    def modify_password(self):
        selected_index = self.password_list.curselection()
        if selected_index:
            selected_index = selected_index[0]
            try:
                with open("passwords.txt", "r") as f:
                    passwords = f.readlines()
                password_parts = passwords[selected_index].split(", ")
                if len(password_parts) == 3:
                    website, username, password = password_parts
                    self.website_entry.delete(0, "end")
                    self.website_entry.insert(0, website.split(": ")[1])
                    self.username_entry.delete(0, "end")
                    self.username_entry.insert(0, username.split(": ")[1])
                    # Store selected password details
                    self.selected_password_index = selected_index
                    self.selected_password_details = password_parts
                    self.password_entry.delete(0, "end")
                    self.password_entry.insert(0, password.split(": ")[1])
                    self.update_button.config(state="normal")  # Enable the Update button
                    # Store the modification change in the recent_changes list
                    self.recent_changes.append(f"Modified - {website}, {username}, {password}")
                else:
                    messagebox.showerror("Error", "Invalid password format")
            except FileNotFoundError:
                pass

    def update_password(self):
        if self.selected_password_index is not None and self.selected_password_details is not None:
            website = self.selected_password_details[0]
            username = self.username_entry.get()
            password = self.password_entry.get()

            updated_password = f"{website}, Username: {username}, Password: {password}\n"

            try:
                with open("passwords.txt", "r") as f:
                    passwords = f.readlines()

                passwords[self.selected_password_index] = updated_password

                with open("passwords.txt", "w") as f:
                    f.writelines(passwords)

                self.display_saved_passwords()
                self.update_button.config(state="disabled")  # Disable the Update button
            except FileNotFoundError:
                pass

    def remove_password(self):
        selected_index = self.password_list.curselection()
        if selected_index:
            selected_index = selected_index[0]
            try:
                with open("passwords.txt", "r") as f:
                    passwords = f.readlines()
                with open("passwords.txt", "w") as f:
                    for i, password in enumerate(passwords):
                        if i != selected_index:
                            f.write(password)
                self.display_saved_passwords()
            except FileNotFoundError:
                pass

    def clear_all_passwords(self):
        try:
            with open("passwords.txt", "w") as f:
                pass  # Clear the file
            self.display_saved_passwords()
            # Store the clearing change in the recent_changes list
            self.recent_changes.append("Cleared all passwords")
        except FileNotFoundError:
            pass
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Historique")

        self.history_listbox = tk.Listbox(history_window, width=50, height=10, bg="white")
        self.history_listbox.pack(padx=20, pady=10, expand=True)

        for entry in self.history_entries:
            self.history_listbox.insert("end", entry)

        for change in self.recent_changes:
            self.history_listbox.insert("end", change)

        clear_button = tk.Button(history_window, text="Clear Logs", command=self.clear_history)
        clear_button.pack(side="left", padx=5, pady=5)

        recover_button = tk.Button(history_window, text="Recover Previous List", command=self.recover_previous_list)
        recover_button.pack(side="left", padx=5, pady=5)

    def clear_history(self):
        self.history_entries.clear()
        self.recent_changes.clear()

    def recover_previous_list(self):
        selected_entry_index = self.history_listbox.curselection()
        if selected_entry_index:
            selected_entry_index = selected_entry_index[0]
            if 0 <= selected_entry_index < len(self.history_entries):  # Check if the index is within valid range
                selected_entry = self.history_entries[selected_entry_index]

                timestamp, saved_data = selected_entry.split(": ", 1)
                timestamp = timestamp.strip()
                saved_data = saved_data.strip()

                try:
                    with open("passwords.txt", "w") as f:
                        f.write(saved_data + "\n")

                    self.display_saved_passwords()
                    messagebox.showinfo("Recovery Success", "Previous list has been recovered.")
                except FileNotFoundError:
                    pass
            else:
                messagebox.showerror("Error", "Please select a valid history entry.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordSaverApp(root)
    root.mainloop()