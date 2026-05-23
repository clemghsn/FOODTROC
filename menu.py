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
        self.img_add = ctk.CTkImage(light_image=Image.open("images/ajouter.png"), size=(200, 65))
        self.img_map = ctk.CTkImage(light_image=Image.open("images/carte.png"), size=(450,75))
        self.img_inventaire = ctk.CTkImage(light_image=Image.open("images/inventaire.png"), size=(200,65))
        self.img_logo= ctk.CTkImage(light_image=Image.open("images/logo.png"), size=(320, 110))
        self.img_deco= ctk.CTkImage(light_image=Image.open("images/logout.png"), size=(215,45))
        self.img_mascotte= ctk.CTkImage(light_image=Image.open("images/mascotte.png"), size=(120,  100))
        self.img_rappel= ctk.CTkImage(light_image=Image.open("images/rappel.png"), size=(215,  45))
        self.switch_page = switch_page
        
        #9DD69A
        self.frame = ctk.CTkFrame(self, corner_radius=30, fg_color='#A0CF9B')
        self.frame.pack(padx = 50, pady=40, fill='both',expand = True)

        self.frame.grid_columnconfigure(0, weight=1)
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
        
        self.button_rappel = ctk.CTkButton(self.frame, text="",image = self.img_rappel, width=0, height=0, fg_color ="transparent", border_width=0)
        self.button_rappel.grid(row=3, column=0,padx = 15, pady=(10,20), sticky="n")

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