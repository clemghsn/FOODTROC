import customtkinter as ctk
from PIL import Image
from ajout import Ajout
from Inventaire import Inventaire
import webbrowser
import csv
from carte import Carte
from datetime import datetime, timedelta
from CTkMessagebox import CTkMessagebox

class Menu(ctk.CTkFrame):
    """
        Cette classe affiche l'interface principale de l'application
        après connexion.

        Elle permet :
            - d'accéder à l'inventaire,
            - d'ajouter un aliment,
            - d'afficher la carte des utilisateurs,
            - de se déconnecter,
            - d'afficher des rappels d'aliments proches de la péremption.
    """
    def __init__(self, master, switch_page):
        """
            Initialise le menu principal.

            Charge les données utilisateurs depuis users.csv
            et construit l'interface graphique (boutons, images, layout).

            Paramètres:
                - master : fenêtre parent (App principale)
                - switch_page (function) : fonction de navigation entre pages.
        """
        super().__init__(master)
        self.switch_page = switch_page
        self.users = self.charger_donnees("users.csv")

        # image
        self.img_add = ctk.CTkImage(light_image=Image.open("images/ajouter.png"), size=(200, 65))
        self.img_map = ctk.CTkImage(light_image=Image.open("images/carte.png"), size=(450,75))
        self.img_inventaire = ctk.CTkImage(light_image=Image.open("images/inventaire.png"), size=(200,65))
        self.img_logo= ctk.CTkImage(light_image=Image.open("images/logo.png"), size=(320, 110))
        self.img_deco= ctk.CTkImage(light_image=Image.open("images/logout.png"), size=(215,45))
        self.img_mascotte= ctk.CTkImage(light_image=Image.open("images/mascotte.png"), size=(120,  100))
        self.img_rappel= ctk.CTkImage(light_image=Image.open("images/rappel.png"), size=(215,  45))
        self.switch_page = switch_page
        
        self.frame = ctk.CTkFrame(self, corner_radius=30, fg_color='#A0CF9B')
        self.frame.pack(padx = 50, pady=40, fill='both',expand = True)

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)

        self.label = ctk.CTkLabel(self.frame, text="",image = self.img_logo )
        self.label.grid(row=0, column=0, columnspan=2, pady=(20,10))

        self.mascotte = ctk.CTkLabel(self.frame, text="",image = self.img_mascotte) 
        self.mascotte.grid(row=4, column=0,columnspan = 2, pady=(10,10), sticky = "n")

        self.button_inventaire = ctk.CTkButton(self.frame, text="",image = self.img_inventaire, width=0, height=0, fg_color ="transparent", border_width=0, command=self.affiche_inventaire)
        self.button_inventaire.grid(row=1, column=0, padx=15, pady=10)

        self.button_add = ctk.CTkButton(self.frame, text="", image = self.img_add, command = self.affiche_ajout, width=0, height=0, fg_color ="transparent", border_width=0)
        self.button_add.grid(row=1, column=1, padx=15, pady=10)

        self.button_carte = ctk.CTkButton(self.frame,text="", image = self.img_map, command = self.affiche_carte, width=0, height=0, fg_color ="transparent", border_width=0)
        self.button_carte.grid(row=2, column=0, columnspan = 2, padx=15, pady=10)

        self.button_logout = ctk.CTkButton(self.frame, text="",image = self.img_deco, command=self.logout, width=0, height=0, fg_color ="transparent", border_width=0)
        self.button_logout.grid(row=3, column=1,padx = 15, pady=(10,20), sticky="n")
        
        self.button_rappel = ctk.CTkButton(self.frame, text="",image = self.img_rappel,command =self.afficher_rappels, width=0, height=0, fg_color ="transparent", border_width=0)
        self.button_rappel.grid(row=3, column=0,padx = 15, pady=(10,20), sticky="n")

    def affiche_carte(self):
        """
            Génère et affiche la carte interactive des utilisateurs.

            Utilise la classe Carte pour créer un fichier HTML
            puis l'ouvre dans le navigateur web par défaut.
        """
        carte = Carte()   # classe folium
        carte.generer()    # méthode qui crée map.html
        webbrowser.open("map.html")

    def affiche_ajout(self):
        """
            Ouvre une nouvelle fenêtre permettant d'ajouter 
            un aliment à l'inventaire.

            Transmet l'utilisateur courant à la fenêtre Ajout.
            """
        new_window = ctk.CTkToplevel(self)
        new_window.title("Ajouter un aliment")
        new_window.geometry("320x350")
        Ajout(new_window, self.master.current_user)

    def affiche_inventaire(self):
        """
            Change la page actuelle vers l'inventaire
            via la fonction de navigation switch_page.
        """
        self.switch_page("inventaire")

    def logout(self):
        """
            Déconnecte l'utilisateur actuel 
            et retourne à la page de login.
        """
        self.switch_page("login")

    def charger_donnees(self, fichier_csv):
        """
            Charge les données utilisateurs depuis un fichier CSV.

            Chaque utilisateur est stocké sous forme de dictionnaire
            contenant son inventaire.

            Paramètres:
                - fichier_csv (str) : chemin du fichier CSV

            Retourne:
                - users (dict) : dictionnaire des utilisateurs
        """

        users = {}

        with open(fichier_csv, mode='r', encoding='utf-8') as f:

            lecteur = csv.DictReader(f)

            for ligne in lecteur:

                users[ligne["id_user"]]= {
                    "inventaire": ligne["inventaire"]
                }

        return users


    def rappels(self):
        """
            Génère une liste de rappels pour les aliments
            proches de la date de péremption (0 à 3 jours).

            Retourne:
                - rappels (list) : messages de rappel
        """
        rappels = []
        inventaire = self.users[self.master.current_user]["inventaire"]

        aliments = inventaire.split("|")
        today = datetime.today()

        for aliment in aliments:
            nom, quantite, date = aliment.split(":")
            date_peremption = datetime.strptime(date, "%d/%m/%Y")
            diff = (date_peremption - today).days + 1

            if 0 <= diff <= 3:

                rappels.append(f"{nom} expire dans {diff} jours")
        return rappels

    def afficher_rappels(self):
        """
            Affiche une notification contenant les rappels d'aliments.

            Utilise CTkMessagebox pour afficher :
                - les aliments proches de la péremption
                - ou un message indiquant qu'il n'y a aucun rappel
        """
        res = self.rappels()

        if res:
            texte = "\n".join(res)
        else:
            texte = "Aucun aliment proche de la péremption"
        
        CTkMessagebox(title="Rappels", message = texte, icon ="warning")

