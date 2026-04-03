import customtkinter as ctk
from tkinter import CENTER



class Login(ctk.CTkFrame):
    def __init__(self, master, switch_page):
        super().__init__(master)

        self.switch_page = switch_page
        
        self.frame = ctk.CTkFrame(self,width=500,height=300,corner_radius=10)
        self.frame.pack()

        self.label = ctk.CTkLabel(self.frame, text="Veuillez vous authentifier", width = 120, height=25, corner_radius=8, font=("Segoe UI", 15))
        self.label.grid(row= 0, column = 0, columnspan = 2, pady=(10,20))

        self.label2 = ctk.CTkLabel(self.frame, text="Identifiant :", width = 120, height=25, corner_radius=8)
        self.label2.grid(row= 1, column = 0, padx=10, pady=10, sticky="e")
        
        self.entry = ctk.CTkEntry(self.frame, width = 120, height=25, corner_radius=10)
        self.entry.grid(row= 1, column = 1, padx=10, pady=10)

        self.label3 = ctk.CTkLabel(self.frame, text="Mot de passe:", width = 120, height=25, corner_radius=8)
        self.label3.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.entry2 = ctk.CTkEntry(self.frame, width = 120, height=25, corner_radius=10, show="*")
        self.entry2.grid(row=2, column=1, padx=10, pady=10)


        self.button = ctk.CTkButton(self.frame, text="Connexion", command = self.login, width=200, height=32, border_width=0, corner_radius=8)
        self.button.grid(row=3, column=0, columnspan=2, pady=20)


    def login(self):
        if self.entry.get() == "admin" and self.entry2.get() == "1234":
            self.switch_page("menu")
        else:
            print("Erreur")
