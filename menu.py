import customtkinter as ctk
from PIL import Image
from Map import Map
from Ajout import Ajout
import webbrowser
from Carte import Carte


class Menu(ctk.CTkFrame):
    def __init__(self, master, switch_page):
        super().__init__(master)
        
        self.switch_page = switch_page

        # image
        self.img_home = ctk.CTkImage(light_image=Image.open("images/home.png"),size=(40,40))
        self.img_add = ctk.CTkImage(light_image=Image.open("images/add.png"),size=(40,40))
        self.img_map = ctk.CTkImage(light_image=Image.open("images/map.png"),size=(40,40))
        self.img_inventaire = ctk.CTkImage(light_image=Image.open("images/inventaire.png"),size=(100,100))
        self.img_foodtroc= ctk.CTkImage(light_image=Image.open("images/foodtroc.png"),size=(300,100))
        self.switch_page = switch_page
        
        self.frame = ctk.CTkFrame(self, width=500, height=300, corner_radius=10)
        self.frame.pack(pady=40)

        for i in range(4):
            self.frame.grid_columnconfigure(i, weight=1)

        self.label = ctk.CTkLabel(self.frame, text="",image = self.img_foodtroc )
        self.label.grid(row=0, column=0, columnspan=4, pady=(10,20))

        self.button_inventaire = ctk.CTkButton(self.frame, text="",image = self.img_inventaire, width=100, height=100, fg_color ="transparent", border_width=0, command=self.affiche_inventaire)
        self.button_inventaire.grid(row=1, column=3, padx=10, pady=20, sticky="ew")

        self.button_home = ctk.CTkButton(self.frame, text="", image = self.img_home, width=50, height=50, fg_color ="transparent", border_width=0)
        self.button_home.grid(row=2, column=0, padx=10, pady=20, sticky="ew")

        self.button_add = ctk.CTkButton(self.frame, text="", image = self.img_add, command = self.affiche_ajout, width=50, height=50, fg_color ="transparent", border_width=0)
        self.button_add.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        self.button_carte = ctk.CTkButton(self.frame,text="", image = self.img_map, command = self.affiche_carte, width=50, height=50, fg_color ="transparent", border_width=0)
        self.button_carte.grid(row=2, column=2, padx=10, pady=20, sticky="ew")

        self.button_logout = ctk.CTkButton(self.frame, text="Déconnexion", command=self.logout)
        self.button_logout.grid(row=2, column=3, padx=10, pady=20, sticky="ew")

    def affiche_carte(self):
        carte = Carte()   # ta classe folium
        carte.generer()    # méthode qui crée map.html
        webbrowser.open("map.html")

    def affiche_ajout(self):
        new_window = ctk.CTkToplevel(self)
        new_window.title("Ajouter un aliment")
        new_window.geometry("320x350")
        Ajout(new_window)

    def affiche_inventaire(self):
        self.switch_page("inventaire")

    def logout(self):
        self.switch_page("login")