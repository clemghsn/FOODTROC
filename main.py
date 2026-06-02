import customtkinter as ctk
from login import Login
from menu import Menu
from inventaire import Inventaire
from posts import Posts
from chat import Chat

ctk.set_default_color_theme("green")

class App(ctk.CTk):
    """
        Classe principale de l'application.

        Elle gère :
            - la fenêtre principale Tkinter
            - la navigation entre les différentes pages (login, menu, inventaire)
            - l'état global de l'utilisateur connecté
            - l'affichage et la destruction des frames
    """
    
    def __init__(self):
        """
            Initialise l'application principale avec :

                - la taille de la fenêtre
                - l'utilisateur courant (non connecté au départ)
                - la frame actuellement affichée
                - puis affiche directement la page de login
        """
        super().__init__()
        self.current_frame = None
        self.current_user = None
        self.show_frame("login")

    def show_frame(self, page):
        """
            Change la page affichée dans l'application.

            Détruit la frame actuelle puis crée la nouvelle
            en fonction du nom de la page demandé.

            Pages disponibles :
                - "login" : page de connexion
                - "menu" : menu principal
                - "inventaire" : gestion de l'inventaire

            Paramètre:
                - page (str) : nom de la page à afficher
        """
        self.geometry("800x650")

        if self.current_frame:
            self.current_frame.destroy()

        if page == "login":
            self.current_frame = Login(self, self.show_frame)

        elif page == "menu":
            self.current_frame = Menu(self, self.show_frame)
        
        elif page == "inventaire":
            self.current_frame = Inventaire(self, self.show_frame)

        elif page == "posts":
            self.current_frame = Posts(self, self.show_frame)

        elif page == "chat":
            self.current_frame = Chat(self, self.show_frame)

        self.current_frame.pack(fill="both", expand=True)

app = App()
app.mainloop()
