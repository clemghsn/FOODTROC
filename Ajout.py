import customtkinter as ctk


class Ajout(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # centrer le contenu
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # carte centrale (effet moderne)
        self.card = ctk.CTkFrame(self, corner_radius=15, width=320, height=350)
        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)


        self.card.grid_columnconfigure(0, weight=1)


        self.title = ctk.CTkLabel(self.card,text="Ajouter un aliment",font=ctk.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 20))

        # Entrée
        self.entry_aliment = ctk.CTkEntry(self.card,placeholder_text="Type d'aliment",height=40)
        self.entry_aliment.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

        self.entry_quantite = ctk.CTkEntry(self.card,placeholder_text="Quantité",height=40)
        self.entry_quantite.grid(row=2, column=0, padx=40, pady=10, sticky="ew")

        self.entry_date = ctk.CTkEntry(self.card,placeholder_text="Date de péremption (JJ/MM/AAAA)",height=40)
        self.entry_date.grid(row=3, column=0, padx=40, pady=10, sticky="ew")

        # Bouton
        self.button_ajouter = ctk.CTkButton(self.card,text="Ajouter",height=45,corner_radius=10,command=self.ajouter_aliment)
        self.button_ajouter.grid(row=4, column=0, padx=40, pady=(20, 20), sticky="ew")

    def ajouter_aliment(self):

        aliment = self.entry_aliment.get()
        quantite = self.entry_quantite.get()
        date = self.entry_date.get()

        print(aliment, quantite, date)
        return (aliment, quantite, date)