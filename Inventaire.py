import customtkinter as ctk


class Inventaire(ctk.CTkFrame):
    
    def __init__(self, master, switch_page):
        super().__init__(master)
        
        self.switch_page = switch_page

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
        aliments = [
            {"nom": "Pomme", "quantite": "2", "date": "12/04"},
            {"nom": "Fromage", "quantite": "1", "date": "10/04"},
        ]

        for aliment in aliments:
            self.create_card(aliment)


    def create_card(self, aliment):
        card = ctk.CTkFrame(self.scroll, corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)

        label_nom = ctk.CTkLabel(card, text=aliment["nom"], font=("Arial", 14, "bold"))
        label_nom.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label_qte = ctk.CTkLabel(card, text=f"Qté: {aliment['quantite']}")
        label_qte.grid(row=0, column=1, padx=10)

        label_date = ctk.CTkLabel(card, text=f"Expire: {aliment['date']}")
        label_date.grid(row=0, column=2, padx=10)
                    
