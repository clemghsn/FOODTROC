import customtkinter as ctk
import csv
from inventaire import Inventaire

class Posts(ctk.CTkFrame):
    """
        Interface graphique permettant d'afficher et gérer
        les alimennts postés par l'utilisateur connecté.

        Cette classe permet :
            - d'afficher les aliments postés
            - de supprimer un aliment
            - de remettre un aliment dans l'inventaire
            - d'incrémenter la quantité de l'aliment
            - de mettre à jour l'affichage dynamiquement
    """
    
    def __init__(self, master, switch_page):
        """
            Initialise la page posts.

            Charge les données utilisateur, récupère l'inventaire 
            du current_user puis affiche les cartes des aliments postés.

            Paramètres:
                - master : fenêtre ou widget parent.
                - switch_page : fonction permettant de changer de page.
        """
        super().__init__(master)
        self.switch_page = switch_page
        self.users = self.charger_donnees("users.csv")
        posts_str = self.users[self.master.current_user]["aliments_postes"]
        self.posts = self.parser_posts(posts_str)

        # centrer le contenu
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0,sticky="ew", padx=20, pady=(20, 10))

        self.header.grid_columnconfigure((0,1,2), weight=1)

        self.title = ctk.CTkLabel(self.header,text="Posts",font=ctk.CTkFont(size=22, weight="bold"))
        self.title.grid(row=0, column=1)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nsew",padx=25, pady=10)
        self.afficher_posts()

        # bouton retour (optionnel)
        self.button_back = ctk.CTkButton(self.header,text="←",width=40,command=lambda: self.switch_page("menu"))
        self.button_back.grid(row=0, column=2, sticky="e")


    def afficher_posts(self):
        """
            Affiche tous les aliments présents
            dans l'inventaire de l'utilisateur.
        """
        for aliment in self.posts:
            self.create_card(aliment)


    def create_card(self, aliment):
        """
            Crée une carte représentant un aliment.

            La carte affiche :
                - le nom
                - la quantité
                - la date de péremption
                - un bouton pour remettre l'aliment dans l'inventaire
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


        # bouton moins
        button_less = ctk.CTkButton(card,text="-",font=("Arial", 16, "bold"), width=3, corner_radius=15, fg_color = "grey", command=lambda a=aliment: self.moins(a))
        button_less.grid(row=0, column=4, padx=(0, 5), pady=5)

        # bouton plus
        button_more = ctk.CTkButton(card,text="+",font=("Arial", 16, "bold"), width=3, corner_radius=15, fg_color = "grey", command=lambda a=aliment: self.plus(a))
        button_more.grid(row=0, column=5, padx=(0, 5), pady=5)



        # bouton retour inventaire
        button_post = ctk.CTkButton(card,text="Retour inventaire",width=40, command=lambda a=aliment: self.retour_inventaire(a))
        button_post.grid(row=0, column=6, padx=(0, 5), pady=5)


        # bouton supprimer
        button_supp = ctk.CTkButton(card,text="Supprimer",width=40, command=lambda a=aliment: self.supprimer(a),fg_color="#E74C3C", hover_color="#C0392B")
        button_supp.grid(row=0, column=7, padx=(0, 10), pady=5)

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

    def parser_posts(self, posts_str):
        """
            Transforme la chaîne de caractères des aliments postés
            en liste de dictionnaires exploitables.

            Paramètre:
                - posts_str (str) : chaîne représentant les aliments postés.

            Retourne:
                - aliments (list) : liste des aliments formatés.
        """

        aliments = []

        if posts_str == "":
            return aliments

        liste = posts_str.split("|")

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
            Supprime un aliment des posts
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

                    posts = ligne.get("aliments_postes", "")
                    aliments = posts.split("|") if posts else []

                    new_list = []

                    for item in aliments:

                        if not item:
                            continue

                        nom, qte, date = item.split(":")

                        if not (nom == aliment["nom"] and date == aliment["date"]):
                            new_list.append(item)

                    ligne["aliments_postes"] = "|".join(new_list)

                users.append(ligne)

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(users)

        self.refresh()
        
    def retour_inventaire(self, aliment):
        """
            Déplace un aliment posté vers l'inventaire 
            de l'utilisateur connecté.

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
                    posts = ligne.get("aliments_postes", "")
                    aliments = posts.split("|") if posts else []

                    new_post = []
                    for item in aliments:

                        if not item:
                            continue

                        nom, qte, date = item.split(":")

                        if not (nom == aliment["nom"] and date == aliment["date"]):
                            new_post.append(item)

                    ligne["aliments_postes"] = "|".join(new_post)

                    # ajouter dans aliments_postes
                    inventaire = ligne.get("inventaire", "")

                    new_inv = f"{aliment['nom']}:{aliment['quantite']}:{aliment['date']}"

                    if inventaire.strip() == "":
                        ligne["inventaire"] = new_inv
                    else:
                        ligne["inventaire"] += "|" + new_inv

                users.append(ligne)

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(users)

        self.refresh()

    def plus(self, aliment):
        """
            Incrémente de 1 la quantité d'un aliment des posts
            de l'utilisateur connecté.

            Le fichier users.csv est ensuite mis à jour
            puis l'interface est rafraîchie.

            Paramètre:
                - aliment (dict) : aliment à modifier
        """

        fichier = "users.csv"
        users = []

        with open(fichier, mode="r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            colonnes = lecteur.fieldnames

            for ligne in lecteur:

                if ligne["id_user"] == self.master.current_user:

                    posts = ligne.get("aliments_postes", "")
                    aliments = posts.split("|") if posts else []

                    new_list = []

                    for item in aliments:

                        if not item:
                            continue

                        nom, qte, date = item.split(":")

                        if not (nom == aliment["nom"] and date == aliment["date"]):
                            new_list.append(item)
                        else :
                            int_qte = int(qte) + 1
                            qte = str(int_qte)
                            item = nom +":"+ qte + ":" + date
                            new_list.append(item)

                    ligne["aliments_postes"] = "|".join(new_list)

                users.append(ligne)

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(users)

        self.refresh()

    def moins(self, aliment) :
        """
            Décrémente de 1 la quantité d'un aliment des posts
            de l'utilisateur connecté.

            Le fichier users.csv est ensuite mis à jour
            puis l'interface est rafraîchie.

            Paramètre:
                - aliment (dict) : aliment à modifier
        """

        fichier = "users.csv"
        users = []

        with open(fichier, mode="r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            colonnes = lecteur.fieldnames

            for ligne in lecteur:

                if ligne["id_user"] == self.master.current_user:

                    posts = ligne.get("aliments_postes", "")
                    aliments = posts.split("|") if posts else []

                    new_list = []

                    for item in aliments:

                        if not item:
                            continue

                        nom, qte, date = item.split(":")

                        if not (nom == aliment["nom"] and date == aliment["date"]):
                            new_list.append(item)
                        else :
                            if qte != "1": 
                                int_qte = int(qte) - 1
                                qte = str(int_qte)
                                item = nom +":"+ qte + ":" + date
                                new_list.append(item)

                    ligne["aliments_postes"] = "|".join(new_list)

                users.append(ligne)

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            writer.writerows(users)

        self.refresh()

    def refresh(self):
        """
            Recharge les données des posts puis met à jour
            l'affichage des cartes dans l'interface graphique.
        """
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.users = self.charger_donnees("users.csv")
        posts_str = self.users[self.master.current_user]["aliments_postes"]
        self.posts = self.parser_posts(posts_str)

        self.afficher_posts()

    

