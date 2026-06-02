import customtkinter as ctk
from aliment import Aliment
from inventaire import Inventaire
import csv
from datetime import datetime

class Ajout(ctk.CTkFrame):
    """
        Fenêtre permettant à un utilisateur d'ajouter un aliment
        à son inventaire personnel.

        Cette interface contient :
            - un champ de saisie du nom de l'aliment,
            - un champ de quantité,
            - un champ de date de péremption,
            - un système de suggestions automatiques,
            - un bouton d'ajout dans le fichier users.csv.
    """

    def __init__(self, master, current_user):
        """
            Initialise la fenêtre d'ajout d'aliment.

            Paramètres:
                - master : fenêtre
                - current_user (str) : identifiant de l'utilisateur connecté.
        """
        super().__init__(master)
        self.current_user = current_user
        self.pack(fill="both", expand=True)

        # centrer le contenu
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # carte centrale 
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
        """
            Récupère les informations saisies par l'utilisateur
            et vérifie leur validité avant l'ajout.

            Vérifications effectuées :
                - tous les champs sont remplis,
                - la date respecte le format JJ/MM/AAAA,
                - la date de péremption n'est pas passée.

            Si les données sont valides :
                - l'aliment est ajouté à l'inventaire,
                - la fenêtre se ferme lors de l'appui du bouton Ajouter
        """
        aliment = self.entry_aliment.get()
        quantite = self.entry_quantite.get()
        date = self.entry_date.get()

        if aliment and quantite and date:
            try: 
                date_peremption = datetime.strptime(date.strip(), "%d/%m/%Y").date()
                today = datetime.today().date()
                if date_peremption < today:
                    print("La date est déjà passée")
                    return
            except ValueError:
                print("Erreur: format de date invalide (JJ/MM/AAAA)")
                return

            self.ajout_inventaire(aliment, quantite, date)
            
            if isinstance(self.master, ctk.CTkToplevel): # ferme la fenêtre de saisie après l'ajout
                self.master.destroy()
        else:
            print("Erreur : Veuillez remplir tous les champs")

    def ajout_inventaire(self, nom, qte, date):
        """
            Ajoute un aliment dans l'inventaire de l'utilisateur courant
            dans le fichier users.csv.

            Si l'aliment existe déjà avec la même date de péremption,
            la quantité est incrémentée.

            Paramètres:
                - nom (str) : nom de l'aliment.
                - qte (int ou str) : quantité de l'aliment.
                - date (str) : date de péremption au format JJ/MM/AAAA.
        """
        fichier = 'users.csv'
        users = []

        qte = int(qte)

        with open(fichier, mode='r', newline='', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            colonnes = lecteur.fieldnames  

            for ligne in lecteur:
                
                ligne.setdefault("inventaire", "")

                if ligne["id_user"] == self.current_user:
                    
                    inventaire = ligne.get("inventaire", "")
                    aliments = inventaire.split("|") if inventaire else []
                    
                    # incrémenter la quantité si même aliment et même date
                    found = False

                    for i in range(len(aliments)):

                        if not aliments[i]:
                            continue
                        
                        try : 
                            n, q, d = aliments[i].split(":")
                            q = int(q)

                            if n == nom and d == date:
                                aliments[i] = f"{n}:{q + qte}:{d}"
                                found = True
                                break

                        except ValueError:
                            continue

                    if not found:
                        aliments.append(f"{nom}:{qte}:{date}")

                    ligne["inventaire"] = "|".join(aliments)

                users.append(ligne)

        with open(fichier, mode='w', newline='', encoding='utf-8') as f:

            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            for user in users:
                writer.writerow(user)

        print(f"{nom} ajouté à l'inventaire de {self.current_user}")

    # Pour le menu déroulant
    def update_suggestions(self, event):
        """
            Met à jour la liste des suggestions d'aliments
            pendant la saisie dans le champ texte.

            Les suggestions proviennent de la méthode
            Aliment.chercher_aliment().

            Paramètre:
                - event : événement clavier déclenché lors de la saisie.
        """
        texte = self.entry_aliment.get().lower()

        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        if texte == "":
            self.suggestion_frame.grid_remove()
            return

        suggestions = Aliment.chercher_aliment(texte)

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
        """
            Insère l'aliment sélectionné dans le champ de saisie
            puis masque la liste des suggestions.

            Paramètre:
                - aliment (str) : aliment choisi par l'utilisateur.
        """

        self.entry_aliment.delete(0, "end")
        self.entry_aliment.insert(0, aliment)

        self.suggestion_frame.grid_remove()