import customtkinter as ctk
import csv

class Inventaire(ctk.CTkFrame):
    
    def __init__(self, master, switch_page):
        super().__init__(master)
        self.switch_page = switch_page
        self.users = self.charger_donnees("users.csv")
        inventaire_str = self.users[self.master.current_user]["inventaire"]
        self.inventaire = self.parser_inventaire(inventaire_str)

        # centrer le contenu
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0,sticky="ew", padx=20, pady=(20, 10))

        self.header.grid_columnconfigure((0,1,2), weight=1)

        self.title = ctk.CTkLabel(self.header,text="Inventaire",font=ctk.CTkFont(size=22, weight="bold"))
        self.title.grid(row=0, column=1)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nsew",padx=20, pady=10)
        self.afficher_inventaire()

        # bouton retour (optionnel)
        self.button_back = ctk.CTkButton(self.header,text="←",width=40,command=lambda: self.switch_page("menu"))
        self.button_back.grid(row=0, column=2, sticky="e")


    def afficher_inventaire(self):
        for aliment in self.inventaire:
            self.create_card(aliment)

    def afficher_inventaire_V2(self):
            try:
                with open('inventaire.csv', mode='r', encoding='utf-8') as f: #mode r=reading
                    lecteur = csv.DictReader(f)
                    for ligne in lecteur:
                        # 'ligne' est maintenant un dico : {"nom": "Pomme", "quantite": "2", ...}
                        self.create_card(ligne)
            except FileNotFoundError: #on teste si le fichier existe pas mais normalement il existe tt le temps c une simulation
                print("Le fichier inventaire.csv n'existe pas encore.")


    def create_card(self, aliment):

        card = ctk.CTkFrame(self.scroll, corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)

        # colonne extensible
        card.grid_columnconfigure(3, weight=1)

        label_nom = ctk.CTkLabel(card,text=aliment["nom"],font=("Arial", 14, "bold"))
        label_nom.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label_qte = ctk.CTkLabel(card,text=f"Qté: {aliment['quantite']}")
        label_qte.grid(row=0, column=1, padx=10)

        label_date = ctk.CTkLabel(card,text=f"Expire: {aliment['date']}")
        label_date.grid(row=0, column=2, padx=10)

        # bouton poster
        button_post = ctk.CTkButton(card,text="+",width=40) #command=self.poster)
        button_post.grid(row=0, column=4, padx=(0, 5), pady=5)


        # bouton supprimer
        button_supp = ctk.CTkButton(card,text="x",width=40) #command=self.supprimer)
        button_supp.grid(row=0, column=5, padx=(0, 10), pady=5)

    def charger_donnees(self, fichier_csv):

        users = {}

        with open(fichier_csv, mode='r', encoding='utf-8') as f:

            lecteur = csv.DictReader(f)


            for ligne in lecteur:

                users[ligne["id_user"]] = {

                    "inventaire": ligne["inventaire"],

                    "aliments_postes": ligne["aliments_postes"]

                }

        return users

    def parser_inventaire(self, inventaire_str):

        aliments = []

        if inventaire_str == "":
            return aliments

        liste = inventaire_str.split("|")

        for item in liste:

            nom, quantite, date = item.split(":")

            aliments.append({
                "nom": nom,
                "quantite": quantite,
                "date": date
            })

        return aliments

    #def supprimer(self):
        
    
    #def poster(self):
