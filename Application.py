import sys
import tkinter as tk
from tkinter import filedialog

class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        # Basic window creation
        self.title("File selector")
        self.geometry("800x600")
    
    def select_file(self) -> str:
        # REMOVE THIS AS SOON AS YOU ADD MORE
        root = tk.Tk()
        root.withdraw()
        # REMOVE THIS AS SOON AS YOU ADD MORE

        file_path = filedialog.askopenfilename(
            title="Select the CSV file to analyse",
            filetypes=(("CSV", "*.csv"), ("All files", "*.*"))
        )
        if not file_path:
            sys.exit()
        return file_path

