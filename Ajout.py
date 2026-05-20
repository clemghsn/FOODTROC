import customtkinter as ctk
from Aliment import Aliment
from Inventaire import Inventaire

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

        # détecter quand on tape
        self.entry_aliment.bind("<KeyRelease>", self.update_suggestions)

        self.suggestion_frame = ctk.CTkFrame(self.card,corner_radius=10,border_width=1)
        

        self.entry_quantite = ctk.CTkEntry(self.card,placeholder_text="Quantité",height=40)
        self.entry_quantite.grid(row=3, column=0, padx=40, pady=10, sticky="ew")

        self.entry_date = ctk.CTkEntry(self.card,placeholder_text="Date de péremption (JJ/MM/AAAA)",height=40)
        self.entry_date.grid(row=4, column=0, padx=40, pady=10, sticky="ew")

        # Bouton
        self.button_ajouter = ctk.CTkButton(self.card,text="Ajouter",height=45,corner_radius=10,command=self.ajouter_aliment)
        self.button_ajouter.grid(row=5, column=0, padx=40, pady=(20, 20), sticky="ew")

    def ajouter_aliment(self):
        """Récupère les données entrées par l'utilisateur"""
        aliment = self.entry_aliment.get()
        quantite = self.entry_quantite.get()
        date = self.entry_date.get()

        if aliment and quantite and date:
            self.ajout_inventaire(aliment, quantite, date)
            
            if isinstance(self.master, ctk.CTkToplevel): # ferme la fenêtre de saisie après l'ajout
                self.master.destroy()
        else:
            print("Erreur : Veuillez remplir tous les champs")

    def ajout_inventaire(self, nom, qte, date):
        """écrit les données dans le fichier inventaire.csv"""
        fichier = 'inventaire.csv'

        with open(fichier, mode='a', newline='', encoding='utf-8') as f: # On ouvre en mode 'a' (append) pour ajouter à la fin mais sans effacer
            colonnes = ['nom', 'quantite', 'date']
            lecteur = csv.DictWriter(f, fieldnames=colonnes)

            lecteur.writerow({
                'nom': nom,
                'quantite': qte,
                'date': date
            })
        print(f"Vous avez ajouté {nom} à {fichier}")
        


    def update_suggestions(self, event):

        texte = self.entry_aliment.get().lower()

        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        if texte == "":
            self.suggestion_frame.grid_remove()
            return

        suggestions = Aliment.chercher_aliment(texte)

        # afficher suggestions
        if suggestions:

            self.suggestion_frame.grid(
                row=2,
                column=0,
                padx=40,
                sticky="ew"
            )

            for aliment in suggestions[:5]:
                button = ctk.CTkButton(self.suggestion_frame,text=aliment,anchor="w",fg_color="transparent",hover_color=("gray80", "gray25"),command=lambda a=aliment: self.select_suggestion(a))
                button.pack(fill="x", padx=5, pady=2)


        else:
            self.suggestion_frame.grid_remove()


    def select_suggestion(self, aliment):

        self.entry_aliment.delete(0, "end")
        self.entry_aliment.insert(0, aliment)

        self.suggestion_frame.grid_remove()