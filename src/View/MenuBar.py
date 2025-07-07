import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Controller.ViewController import ViewController

class MenuBar(tk.Menu):
    def __init__(self, parent:"ViewController"):
        super().__init__(parent)
        self.view_controller = parent
        
        # File menu
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Choisir projet",
                              command=lambda: parent.call_set_project_path())
        self.add_cascade(label="Fichier", menu=file_menu)
        
        # Analyse menu
        analyse_menu = tk.Menu(self, tearoff=0)
        analyse_menu.add_command(label="Nouvelle Analyse - CSV", 
                              command=lambda: parent.call_analyse_csv())
        analyse_menu.add_command(label="Novelle Analyse - RAW",
                              command=lambda: parent.call_analyse_raw())
        analyse_menu.add_separator()
        analyse_menu.add_command(label="Commencer mesure",
                                 command= lambda: parent.call_mesure())
        analyse_menu.add_command(label="Arrêter mesure",
                                 command= lambda: parent.call_stop_mesure())
        self.add_cascade(label="Analyse", menu=analyse_menu)
        
        # Tutorial menu
        tuto_menu = tk.Menu(self, tearoff=0)
        tuto_menu.add_command(label="Introduction",
                              command= self.tuto_intro)
        tuto_menu.add_command(label="Analyse de CSV/RAW",
                              command= self.tuto_analyse)
        tuto_menu.add_command(label="Prise de mesure",
                              command=self.tuto_record)
        self.add_cascade(label="Tutoriel", menu=tuto_menu)
        
        # Debug program
        #debug_menu = tk.Menu(self, tearoff=0)
        #debug_menu.add_command(label="Get window dimentions",
        #                       command=lambda: parent.get_window_dim())
        #self.add_cascade(label="Debug", menu=debug_menu)
        
        # Credit
        self.add_command(label="À propos", command=self.credit_view)
        
        # Close program
        self.add_command(label="Fermer", command=lambda: self.exit(self.view_controller))
        
    def tuto_intro(self):
        content = [
            {"title": "Bienvenu à vous!",
             "text" : "Merci d'utiliser FLASHy pour vos analyses de pulse! Le programme contient deux principales fonctionnalités\n\t- Prise de données\n\t- Analyse de pulses\n"+
                      "Dans ce tutoriel, nous allons les explorer.",
             "image": os.path.join("images", "intro-1.png")},
            {"title": "Tab 1 - Informations et Bypass",
             "text" : "Ce tab contient tout ce qui tout ce qui est lié au digitizer, passant par la modification de ses paramètres à la prise de données. Aussi, il est possible de modifier les paramètres des DataAnalyser dans le sous-tab Analyse.\n"+
                      "Si la souris se trouve sur le nom d'un paramètre, une description de ce paramètre est affichée. De plus, il est possible de changer quels paramètres sont envoyés au digitizer en faisant un clic droit (Ne fonctionne pas).",
             "image": os.path.join("images", "intro-2.png")},
            {"title": "Tab 2 et 3 - Prises de mesures",
             "text" : "Les tabs CH0 et CH1 ont la fonctionnalité d'analyser des pulses suites à la prise de mesure. Ils contiennent un GraphShowcase et un DataAnalyser associé. Le DataAnalyser s'occupe d'analyser les pulses qui lui sont envoyé. Le GraphShowcase est responsable d'afficher les graphiques et la liste des aires des pulses.\n"+
                      "Des fichiers CSV et RAW sont enregistrés pour chaque canal dans le dossier nommé 'DAQ' (voir le tutoriel pour l'analyse)",
             "image": os.path.join("images", "intro-3.png")},
            {"title": "Tab 4 et 5 - Lecture de CSV/RAW",
             "text" : "Comme CH0 et CH1, ces deux tabs permettent d'afficher l'analyse de pulses, la différence étant que ceux-ci analysent les pulses contenu dans un fichier csv ou un fichier raw.\n"+
                      "De plus, vous n'êtes pas obligés d'analyser des RAW dans le tab 'Lecture RAW' et pouvez y analyser des CSV si cela vous plait. (NOTE: l'analyse de fichiers RAW ne fonctionnent pas)",
             "image": os.path.join("images", "intro-4.png")},
            {"title": "Section Feedback",
             "text" : "Au cours des prises de mesures et de l'utilisation de FLASHy, le programme vous avisera des changements que vous faites et de ce qu'il est en train de calculer. Il peut être alors intéressant d'enregistrer les traces de vos expériences, d'où le bouton 'Sauvegarder Feedback'.\n"+
                      "Ils seront enregistés dans le fichier 'Feedback' qui se retrouve dans le dossier du programme (voir le tutoriel pour l'analyse)",
             "image": os.path.join('images', "intro-5.png")}
        ]
        TutorialWindow(self.view_controller.root, self.view_controller, content)
    
    def tuto_analyse(self):
        content = [
            {"title": "Analyse de données - CSV et RAW",
             "text" : "Dans ce tutoriel, vous allez apprendre comment utiliser les tabs 'Lecture CSV' et 'Lecture RAW'",
             "image": os.path.join("images", "intro-4.png")},
            {"title": "Sélection de fichier - Ouvrir un fichier",
             "text" : "Rendez-vous dans un des tabs contenant une barre comme celle-ci.\nPour ouvrir un nouveau fichier cliquer sur le bouton 'Ouvrir'. Une fenêtre s'ouvrira vous demandant de sélectionner un fichier pour l'analyse. Trouver le dossier où FLASHy a été installé; il devrait ressembler à ceci.",
             "image": os.path.join("images", "analyse-2.png")},
            {"title": "Sélection de fichier - CSV",
             "text" : "Pour trouver les fichiers que FLASHy enregistrent après une prise de mesure, il faut suivre ce chemin:\n\nDAQ --> open_on_{la date} --> {le nom du shoot + increment}\n\nCe fichier contiendra deux CSV et deux RAW ainsi qu'un fichier TXT contenant les paramètres de ce shoot.\n"+
                      "Il est aussi possible d'ouvrir un fichier CSV généré par CoMPASS; FLASHy va le reconnaitre et l'analyser de la même manière que ces propres CSV",
             "image": os.path.join("images", "analyse-3.png")},
            {"title": "Sélection de fichier - RAW",
             "text" : "Les fichiers RAW peuvent aussi être analyser (ne fonctionnent pas). L'avantage de ces fichiers sont qu'ils contiennent tout ce que le digitizer a lu, incluant les moments ne contenant pas de pulses. Ceci peut être utile pour débugger s'il manque des pulses.",
             "image": os.path.join("images", "analyse-3.png")},
            {"title": "Analyse et affichage des résultats",
             "text" : "Une fois un fichier sélectionné, il suffit de confirmer que le fichier est celui voulu. Son path sera affiché dans la console Feedback et à gauche des boutons. Cliquez sur 'Analyser' pour voir les résultats!",
             "image": os.path.join("images", "intro-1.png")},
        ]
        TutorialWindow(self.view_controller.root, self.view_controller, content)
    
    def tuto_record(self):
        content = [
            {"title": "Prise de données - Digitizer DT5781",
             "text" : "Dans ce tutoriel, vous allez apprendre à prendre des nouvelles mesures et voir l'analyse de pulses\n\n"+
                      "NOTE: La prise de mesure fonctionne seulement à l'aide d'un digitizer CAEN DT5781",
             "image": os.path.join("images", "record-1.png")},
            {"title": "Connection au Digitizer",
             "text" : "D'abord, connecter le digitizer à votre ordinateur et cliquer sur 'Connecter au Digitizer'. Si tout va bien, des informations sur le Digitizer seront affichées",
             "image": os.path.join("images", "record-2.png")},
            {"title": "Début de la prise de mesure",
             "text" : "Ensuite, renommer le shoot au besoin. Notez que les noms ne sont pas enregistrés après la fermeture du programme, ce qui veut dire qu'il faut renommer à l'ouverture pour éviter d'effacer des anciennes mesures.\n"+
                      "De plus, vous pouvez garder le même nom pour plusieurs prises de mesure puisque FLASHy incrémente automatiquement le nom. Par exemple, si vous nommez vos shoots 'test', les fichiers seront 'test_1', 'test_2', ect.\n"+
                      "Cliquer sur 'Commencer mesure' lorsque vous êtes prêt.",
             "image": os.path.join("images", "record-3.png")},
            {"title": "Pendant la prise de mesure",
             "text" : "Une fois partie, FLASHy commencera à lire les données du Digitizer et affichera ce qu'il lit en temps réel dans une autre fenêtre. La fermeture de cette fenêtre arrêtera la prise de mesure. Vous pouvez cliquer sur 'Arrêter mesure' pour l'arrêter\n",
             "image": os.path.join("images", "record-4.png")},
            {"title": "Après la prise de mesure",
             "text" : "Une fois terminée, FLASHy enregistera deux CSV et deux RAW (un de chaque type pour chaque canal) ainsi que les paramètres utilisés pour le shoot. Ils se retrouvent dans le fichier ayant le nom choisi précédemment. (voir le tutoriel d'analyse pour plus d'information)\n"+
                      "Les résultats sont aussi affichés dans les tabs 'CH0' et 'CH1'.",
             "image": os.path.join("images", "record-5.png")},
        ]
        TutorialWindow(self.view_controller.root, self.view_controller, content)
    
    def credit_view(self):
        content = [
            {"title": "À propos",
             "text" : "FLASHy a été créé en Automne 2024 par Jean-Emmanuel Chouinard dans le cadre de son projet de fin d'études au baccalauréat à l'Université de Montréal sous la supervision d'Arthur Lalonde.",
             "image": os.path.join("images", "intro-1.png")},
            {"title": "Remerciements",
             "text" : "Arthur Lalonde, pour l'opportunité de faire parti de son équipe de recherche\nJavier Chiasson, pour avoir opéré le Mobetron pour mes multiples tests\nDominique Guillet, pour avoir opéré le Mobetron pour mes derniers tests\nL'entièreté de l'équipe FLASH",
             "image": os.path.join("images", "intro-1.png")},
        ]
        TutorialWindow(self.view_controller.root, self.view_controller, content)
        
    def exit(self, view_controller) -> None:
        # Do a pop-up confirmation
        check = CustomDialog(view_controller, "Quitter le programme?", "Oui", "Non")
        if check.result:
            self.view_controller.controller.save_parameters()
            view_controller.quit()


# Used for confirming quitting the program via the Menu bar
class CustomDialog(tk.Toplevel):
    def __init__(self, parent, message:str, yes_text:str, no_text:str):
        self.view_controller = parent
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

# Used for tutorials
class TutorialWindow:
    def __init__(self, parent, view_controller:"ViewController", tutorial_content):
        self.view_controller = view_controller
        self.tutorial_content = tutorial_content
        self.current_index = 0

        self.window = tk.Toplevel(parent)
        self.window.title("Tutoriel")
        self.window.geometry("525x750")

        # Title label
        self.title_label = ttk.Label(self.window, text="", font=("Arial", 16, "bold"), style=self.view_controller.style.label_style)
        self.title_label.grid(row=0, column=0, sticky='nswe')

        # Text area
        self.text_area = tk.Text(self.window, wrap=tk.WORD, height=10, width=50, font=("Arial", 12))
        self.text_area.grid(row=1, column=0, sticky='nswe', pady=10, padx=10)
        self.text_area.tag_configure("left", justify="left")
        self.text_area.config(state=tk.DISABLED)

        # Image display
        self.image_label = ttk.Label(self.window, style=self.view_controller.style.label_style)
        self.image_label.grid(row=2, column=0, sticky='nswe', pady=10, padx=10)

        # Navigation buttons
        self.button_frame = ttk.Frame(self.window, style=self.view_controller.style.tframe_style)
        self.button_frame.grid(row=3, column=0, sticky='nswe', pady=10, padx=10)

        self.prev_button = ttk.Button(self.button_frame, text="Précédent", command=self.show_previous, style=self.view_controller.style.button_style)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = ttk.Button(self.button_frame, text="Prochain", command=self.show_next, style=self.view_controller.style.button_style)
        self.next_button.grid(row=0, column=1, padx=5)
        
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.update_content()

    def update_content(self):
        content = self.tutorial_content[self.current_index]

        # Update title
        self.title_label.config(text=content['title'])

        # Update text
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content['text'])
        self.text_area.tag_add("left", "1.0", "end")
        self.text_area.config(state=tk.DISABLED)

        # Update image
        image = Image.open(content['image'])
        image = image.resize((500, 400))  # Resize to fit
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)

        # Update button states
        self.prev_button.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_index < len(self.tutorial_content) - 1 else tk.DISABLED)

    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_content()

    def show_next(self):
        if self.current_index < len(self.tutorial_content) - 1:
            self.current_index += 1
            self.update_content()