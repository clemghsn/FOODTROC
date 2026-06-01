import customtkinter as ctk
from tkinter import CENTER
import csv



class Login(ctk.CTkFrame):
    def __init__(self, master, switch_page):
        super().__init__(master)
        self.users = self.charger_donnees("users.csv")

        self.switch_page = switch_page
        
        self.frame = ctk.CTkFrame(self,width=300,height=300,corner_radius=10)
        self.frame.pack()

        self.label = ctk.CTkLabel(self.frame, text="Veuillez vous authentifier", width = 150, height=50, corner_radius=8, font=("Segoe UI", 19))
        self.label.grid(row= 0, column = 0, columnspan = 2, pady=(10,20))

        self.label2 = ctk.CTkLabel(self.frame, text="Identifiant :", width = 150, height=50, corner_radius=8, font=("Segoe UI", 17))
        self.label2.grid(row= 1, column = 0, padx=10, pady=10, sticky="we")
        
        self.entry = ctk.CTkEntry(self.frame, width = 170, height=35, corner_radius=10)
        self.entry.grid(row= 1, column = 1, padx=10, pady=10)

        self.label3 = ctk.CTkLabel(self.frame, text="Mot de passe:", width = 120, height=25, corner_radius=8, font=("Segoe UI", 17))
        self.label3.grid(row=2, column=0, padx=10, pady=10, sticky="we")
        
        self.entry2 = ctk.CTkEntry(self.frame, width = 170, height=35, corner_radius=10, show="*")
        self.entry2.grid(row=2, column=1, padx=10, pady=10)

        self.button = ctk.CTkButton(self.frame, text="Connexion", command = self.login, width=200, height=32, border_width=0, corner_radius=8, font=("Segoe UI", 15))
        self.button.grid(row=3, column=0, columnspan=2, pady=20)

    def charger_donnees(self, fichier_csv):

        users = {}

        with open(fichier_csv, mode='r', encoding='utf-8') as f:

            lecteur = csv.DictReader(f)
            print(lecteur.fieldnames)

            for ligne in lecteur:

                users[ligne["id_user"]]= {
                    "mdp": ligne["password"],
                }

        return users

    def login(self):
        identifiant = self.entry.get()
        mdp = self.entry2.get()
        if identifiant in self.users and mdp == self.users[identifiant]["mdp"]:
            print("Connexion réussie")
            self.master.current_user = identifiant
            self.switch_page("menu")
        else:
            print("Erreur")
