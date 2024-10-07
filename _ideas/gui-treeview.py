import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Treeview Example")
root.geometry("400x300")

# Create a Treeview widget
tree = ttk.Treeview(root)

# Insert parent items (e.g., folders)
parent1 = tree.insert("", tk.END, text="Folder 1")
parent2 = tree.insert("", tk.END, text="Folder 2")

# Insert child items (e.g., files)
tree.insert(parent1, tk.END, text="File 1.1")
tree.insert(parent1, tk.END, text="File 1.2")
tree.insert(parent2, tk.END, text="File 2.1")

# Pack the treeview to make it visible
tree.pack(expand=True, fill="both")

# Start the Tkinter event loop
root.mainloop()
