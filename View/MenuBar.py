import tkinter as tk
from tkinter import ttk

class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Analyse menu
        analyse_menu = tk.Menu(self, tearoff=0)
        analyse_menu.add_command(label="Nouvelle Analyse", 
                              command=lambda: parent.call_file_selector())
        analyse_menu.add_command(label="Ouvrir Analyse",
                              command=lambda: parent.call_open_data())
        analyse_menu.add_command(label="Sauvegarder Analyse",
                                 command=lambda: parent.call_save_data())
        self.add_cascade(label="Analyse", menu=analyse_menu)
        
        # Settings menu
        setting_menu = tk.Menu(self, tearoff=0)
        setting_menu.add_command(label="Changer Record Lenght",
                              command=lambda: parent.call_change_rcd_len())
        setting_menu.add_command(label="Changer Pre Trigger",
                              command=lambda: parent.call_change_pre_trig())
        self.add_cascade(label="Préférence", menu=setting_menu)
        
        # Debug program
        debug_menu = tk.Menu(self, tearoff=0)
        debug_menu.add_command(label="Get window dimentions",
                               command=lambda: parent.get_window_dim())
        self.add_cascade(label="Debug", menu=debug_menu)
        
        # Close program
        self.add_command(label="Fermer", command=lambda: self.exit(parent))
        
        
    def exit(self, parent) -> None:
        # Do a pop-up confirmation
        check = CustomDialog(parent, "Quitter le programme?", "Oui", "Non")
        if check.result:
            parent.quit()


# Used for confirming quitting the program via the Menu bar
class CustomDialog(tk.Toplevel):
    def __init__(self, parent, message:str, yes_text:str, no_text:str):
        super().__init__(parent)
        self.geometry("+100000+100000")
        self.result = None
        self.title("Confirmer fermeture") 
        
        # Create the label for the message
        label = tk.Label(self, text=message)
        label.pack(pady=10)

        # Create Yes button
        yes_button = ttk.Button(self, text=yes_text, command=self.on_yes)
        yes_button.pack(side="left", padx=20, pady=20)

        # Create No button
        no_button = ttk.Button(self, text=no_text, command=self.on_no)
        no_button.pack(side="right", padx=20, pady=20)
        
        # Centered on the parent's window
        self.center_window(parent)
        
        # Wait for the window to close
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
        
    def center_window(self, parent) -> None:
        self.update_idletasks()  # Ensure window is updated to get the correct size
        popup_width = self.winfo_reqwidth()
        popup_height = self.winfo_reqheight()

        # Get the parent window's position and size
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calculate position for the popup to be centered
        center_x = parent_x + (parent_width // 2) - (popup_width // 2)
        center_y = parent_y + (parent_height // 2) - (popup_height // 2)

        # Set the position of the popup window
        self.geometry(f"+{center_x}+{center_y}")

    def on_yes(self) -> None:
        self.result = True
        self.destroy()  # Close the dialog

    def on_no(self) -> None:
        self.result = False
        self.destroy()  # Close the dialog
