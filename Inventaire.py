import customtkinter as ctk
import csv

class Inventaire(ctk.CTkFrame):
    """
        Interface graphique permettant d'afficher et gérer
        l'inventaire de l'utilisateur connecté.

        Cette classe permet :
            - d'afficher les aliments de l'inventaire
            - de supprimer un aliment
            - de poster un aliment
            - de mettre à jour l'affichage dynamiquement
    """
    
    def __init__(self, master, switch_page):
        """
            Initialise la page inventaire.

            Charge les données utilisateur, récupère l'inventaire 
            du current_user puis affiche les cartes des aliments.

            Paramètres:
                - master : fenêtre ou widget parent.
                - switch_page : fonction permettant de changer de page.
        """
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
        """
            Affiche tous les aliments présents
            dans l'inventaire de l'utilisateur.
        """
        for aliment in self.inventaire:
            self.create_card(aliment)


    def create_card(self, aliment):
        """
            Crée une carte représentant un aliment.

            La carte affiche :
                - le nom
                - la quantité
                - la date de péremption
                - un bouton pour poster l'aliment
                - un bouton pour supprimer l'aliment

            Paramètres:
                aliment (dict) : dictionnaire contenant
                les informations de l'aliment.
        """

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
        button_post = ctk.CTkButton(card,text="Poster",width=40, command=lambda a=aliment: self.poster(a))
        button_post.grid(row=0, column=4, padx=(0, 5), pady=5)


        # bouton supprimer
        button_supp = ctk.CTkButton(card,text="Supprimer",width=40, command=lambda a=aliment: self.supprimer(a),fg_color="#E74C3C", hover_color="#C0392B")
        button_supp.grid(row=0, column=5, padx=(0, 10), pady=5)

    def charger_donnees(self, fichier_csv):
        """
            Charge les données des utilisateurs depuis un fichier CSV.

            Les informations récupérées sont :
                - l'inventaire
                - les aliments postés

            Paramètre:
                - fichier_csv (str) : chemin du fichier CSV.

            Retourne:
                - users (dict) : dictionnaire contenant les données utilisateurs.
        """

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
        """
            Transforme la chaîne de caractères de l'inventaire
            en liste de dictionnaires exploitables.

            Paramètre:
                - inventaire_str (str) : chaîne représentant l'inventaire.

            Retourne:
                - aliments (list) : liste des aliments formatés.
        """

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

    def supprimer(self, aliment):
        """
            Supprime un aliment de l'inventaire
            de l'utilisateur connecté.

            Le fichier users.csv est ensuite mis à jour
            puis l'interface est rafraîchie.

            Paramètre:
                - aliment (dict) : aliment à supprimer
        """

        fichier = "users.csv"
        users = []

        with open(fichier, mode="r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            colonnes = lecteur.fieldnames

            for ligne in lecteur:

                if ligne["id_user"] == self.master.current_user:

                    inventaire = ligne.get("inventaire", "")
                    aliments = inventaire.split("|") if inventaire else []

                    new_list = []

                    for item in aliments:

                        if not item:
                            continue

                        nom, qte, date = item.split(":")

                        if not (nom == aliment["nom"] and date == aliment["date"]):
                            new_list.append(item)

                    ligne["inventaire"] = "|".join(new_list)

                users.append(ligne)

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(users)

        self.refresh()
        
    def poster(self, aliment):
        """
            Déplace un aliment de l'inventaire vers la liste 
            des aliments postés de l'utilisateur connecté.

            Le fichier users.csv est mis à jour puis l'affichage 
            est rafraîchi.

            Paramètre:
                - aliment (dict) : aliment à poster.
        """

        fichier = "users.csv"
        users = []

        with open(fichier, mode="r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            colonnes = lecteur.fieldnames

            for ligne in lecteur:

                if ligne["id_user"] == self.master.current_user:

                    # enlever inventaire
                    inventaire = ligne.get("inventaire", "")
                    aliments = inventaire.split("|") if inventaire else []

                    new_inv = []
                    for item in aliments:

                        if not item:
                            continue

                        nom, qte, date = item.split(":")

                        if not (nom == aliment["nom"] and date == aliment["date"]):
                            new_inv.append(item)

                    ligne["inventaire"] = "|".join(new_inv)

                    # ajouter dans aliments_postes
                    postes = ligne.get("aliments_postes", "")

                    new_post = f"{aliment['nom']}:{aliment['quantite']}:{aliment['date']}"

                    if postes.strip() == "":
                        ligne["aliments_postes"] = new_post
                    else:
                        ligne["aliments_postes"] += "|" + new_post

                users.append(ligne)

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(users)

        self.refresh()

    def refresh(self):
        """
            Recharge les données de l'inventaire puis met à jour
            l'affichage des cartes dans l'interface graphique.
        """
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.users = self.charger_donnees("users.csv")
        inventaire_str = self.users[self.master.current_user]["inventaire"]
        self.inventaire = self.parser_inventaire(inventaire_str)

        self.afficher_inventaire()
