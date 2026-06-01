import tkinter as tk
from tkinter import LabelFrame, ttk

# File for setting up custom styles for the program

# Useful colors
LIGHT_GRAY = "#f0f0f0"
GRAY = "#bdbdbd"
DARK_GRAY = "#636363"
BLACK = "#000000"
WHITE = "#FFFFFF"
BUTTON = "#E1E1E1"

# Font
FONT = ("Arial", 12, "normal")

class FLASHyStyle(ttk.Style):
    # Useful colors
    LIGHT_GRAY = "#f0f0f0"
    GRAY = "#bdbdbd"
    DARK_GRAY = "#636363"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    BUTTON = "#E1E1E1"
    
    # Font
    FONT = ("Arial", 12, "normal")
    
    def __init__(self, root) -> None:
        super().__init__(root)
        self.theme_use("alt")
        
        self.notebook_style = "CustomNotebook"
        self.maintabs_style = "CustomNotebook.Tab"
        self.tframe_style = "CustomTFrame"
        self.label_style = "CustomLabel"
        self.button_style = "CustomButton"
        self.entry_style = "CustomEntry"
        
        self.layout(self.notebook_style, self.layout("TNotebook"))
        self.layout(self.maintabs_style, self.layout("TNotebook.Tab"))
        self.layout(self.tframe_style, self.layout("TFrame"))
        self.layout(self.label_style, self.layout("TLabel"))
        self.layout(self.button_style, self.layout("TButton"))
        self.layout(self.entry_style, self.layout("TEntry"))
        
        self.configure_notebook()
        self.configure_tabs()
        self.configure_tframe()
        self.configure_label()
        self.configure_button()
        self.configure_entry()
        
    def configure_notebook(self):
        self.configure(
            self.notebook_style,
            background=LIGHT_GRAY,  # Background color for the notebook
            borderwidth=0,          # Width of the notebook border
            relief="raised",        # Border style
            padding=0              # Padding around the notebook area
            )              
        
    def configure_tabs(self):
        # Base tab style (non-selected state)
        self.configure(
            self.maintabs_style,
            background=BUTTON,      # Background color for unselected tabs
            foreground=BLACK,           # Text color for unselected tabs
            #font=FONT,                  # Font for tab text
            padding=[4, 2],             # Padding around the text
            borderwidth=2,              # Tab border width
            relief="raised"             # Tab border style
        )

        # Map additional states such as selected and hover (active)
        self.map(
            self.maintabs_style,
            background=[("selected", LIGHT_GRAY), ("active", LIGHT_GRAY)],
            foreground=[("selected", BLACK), ("active", BLACK)]
        )
    
    def configure_tframe(self):
        self.configure(
            self.tframe_style,
            background=LIGHT_GRAY
        )
        
    def configure_button(self):
        self.configure(
            self.button_style,
            background=BUTTON,
            foreground=BLACK,
            relief="raised",
            borderwidth=2,
            anchor=tk.CENTER,
            padding=[10, 2]
        )
        
        self.map(
            self.button_style,
            background=[("active", LIGHT_GRAY)],
            relief=[("pressed", 'sunken')]
        )
        
    def configure_label(self):
        self.configure(
            self.label_style,
            background=LIGHT_GRAY,
            padding=[2, 5]
        )
    
    def configure_entry(self):
        self.configure(
            self.entry_style,
            background=LIGHT_GRAY,
            padding=[2, 5]
        )
    
    def apply_style_notebook(self, notebook:ttk.Notebook):
        notebook.configure(style=self.notebook_style)
    def apply_style_tframe(self, tframe:ttk.Frame):
        tframe.configure(style=self.tframe_style)