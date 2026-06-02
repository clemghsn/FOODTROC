import customtkinter as ctk
from aliment import Aliment
from inventaire import Inventaire
import csv
from PIL import Image
from datetime import datetime
from conversation import Conversation

class Chat(ctk.CTkFrame):
    """
        Fenêtre permettant à un utilisateur d'accéder à ses conversations avec les autres utilisateurs.

        Cette classe permet :
            - d'afficher les conversations de l'utilisateur
            - de rechercher un utilisateur pour démarrer une nouvelle conversation
    """

    def __init__(self, master, switch_page):
        """
            Initialise la fenêtre de messagerie.

            Paramètres:
                - master : fenêtre
                - current_user (str) : identifiant de l'utilisateur connecté.
        """
        super().__init__(master)
        self.switch_page = switch_page

        #récupération des conversations et utilisateurs
        self.chat, self.chat_user = self.charger_conv("chat.csv")
        self.users = self.charger_donnees("users.csv")

        # image

        self.img_bin = ctk.CTkImage(Image.open("images/poubelle.png"), size=(18, 18))

        # centrer le contenu
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0,sticky="ew", padx=25, pady=(20, 10))
        self.header.grid_columnconfigure(1, weight=1)
 
        self.title = ctk.CTkLabel(self.header,text="Messagerie",font=ctk.CTkFont(size=22, weight="bold"))
        self.title.grid(row=0, column=1)

        # Bouton retour
        self.button_back = ctk.CTkButton(self.header,text="←",width=40,command=lambda: self.switch_page("menu"))
        self.button_back.grid(row=0, column=2, sticky="e")

        # Search Frame

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=2, column=0, sticky="ew", padx=25)
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.label_new = ctk.CTkLabel(self.search_frame,text="Nouvelle conversation",font=("Arial", 14, "bold"))
        self.label_new.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=5)

        # Entrée + bouton

        self.entry_user = ctk.CTkEntry(self.search_frame,placeholder_text="Recherche utilisateur")
        self.entry_user.grid(row=1, column=0, sticky="ew", padx= 15, pady = (0,10))
        self.entry_user.bind("<FocusIn>", self.update_suggestions)

        self.button_new = ctk.CTkButton(self.search_frame, text="Ecrire",width=120,command=self.afficher_new_conv)
        self.button_new.grid(row=1, column=1, padx= 15, pady=(0,10))


        # Conversations
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=3, column=0, sticky="nsew", padx=25, pady=10)
        self.afficher_chat()

        self.suggestion_frame = ctk.CTkFrame(self.search_frame)
        self.suggestion_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        self.suggestion_frame.grid_remove()

    def charger_conv(self, fichier_csv):
        """
            Charge les conversations des utilisateurs depuis un fichier CSV.

            Les informations récupérées sont :
                - l'inventaire
                - les aliments postés

            Paramètre:
                - fichier_csv (str) : chemin du fichier CSV.

            Retourne:
                - chat(list) : liste de tous les messages enregistés
                - conv (dict) : dictionnaire contenant les conversation de l'utilisateur connecté.
        """

        conv = {}
        chat = []

        with open(fichier_csv, mode='r', encoding='utf-8') as f:

            lecteur = csv.DictReader(f)

            for ligne in lecteur:
                
                chat.append(ligne)

                if ligne["sender"] == self.master.current_user:
                    message = conv.get(ligne["receiver"],"")
                    text = ligne["messages"]
                    print(text)
                    message = f"{message}|{text}:envoyé"
                    conv[ligne["receiver"]] = message
                    
                elif ligne["receiver"] == self.master.current_user:
                    message = conv.get(ligne["sender"],"")
                    text = ligne["messages"]
                    message = f"{message}|{text}:reçu"
                    conv[ligne["sender"]] = message
            

        return chat, conv
    
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
                users[ligne["id_user"]] = ligne
        return users
    
    def afficher_chat(self):
        """
            Affiche tous les conversations de l'utilisateur.
        """
        for user2 in self.chat_user.keys():
            self.create_card(user2)

        if len(self.chat_user.keys()) == 0:
            self.label = ctk.CTkLabel(self.scroll,text="Aucune conversation",font=("Arial", 16, "bold"))
            self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    def create_card(self, user2):
        """
            Crée une carte représentant une conversation.

            La carte affiche :
                - le nom de l'interlocuteur (user2)
                - un bouton pour supprimer la conversation
               
            Paramètres:
                conv (dict) : dictionnaire contenant
                les informations de la conversation.
        """

        card = ctk.CTkFrame(self.scroll, corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)

        # colonne extensible
        card.grid_columnconfigure(3, weight=1)

        label_nom = ctk.CTkLabel(card,text=user2,font=("Arial", 14, "bold"))
        label_nom.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        button_ouvrir = ctk.CTkButton(card,text="Ouvrir",font=("Arial", 12, "bold"), width=3, corner_radius=15, fg_color = "grey", command=lambda a=user2: self.afficher_conv(a))
        button_ouvrir.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="e")
    
        button_supprimer = ctk.CTkButton(card,text="", image = self.img_bin, width=3, corner_radius=15, fg_color = "transparent", command=lambda a=user2: self.suppr_conv(a))
        button_supprimer.grid(row=0, column=2, padx=(0, 3), pady=5, sticky="e")

    def afficher_conv(self, user2):
        """
            Ouvre une nouvelle fenêtre permettant d'envoyer des messages aux autres utilisateurs.

            Transmet l'utilisateur courant à la fenêtre Conversation.
            """
        new_window = ctk.CTkToplevel(self)
        new_window.title(user2)
        new_window.geometry("350x450")
        Conversation(new_window, self.master.current_user, user2, self.chat_user[user2])

    def suppr_conv(self, user2):
        """
            Supprime la conversation avec l'utilisateur user2 dans le fichier chat.csv
            """
        
        fichier = "chat.csv"
        messages = []

        for ligne in self.chat:

                if (ligne["sender"] == self.master.current_user and ligne["receiver"] == user2) or (ligne["receiver"] == self.master.current_user and ligne["sender"] == user2):
                    continue #on continue, la ligne n'est pas sauvegardée

                else :
                    sender = ligne["sender"]
                    receiver = ligne["receiver"]
                    text = ligne["messages"]

                    

                messages.append({
                    "sender" : sender,
                    "receiver" : receiver,
                    "messages" : text
                })

        with open(fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["sender","receiver","messages"])
            writer.writeheader()
            writer.writerows(messages)

        self.refresh()

    def refresh(self):
        """
            Recharge les données de la messagerie puis met à jour
            l'affichage des cartes dans l'interface graphique.
        """
        for widget in self.scroll.winfo_children():
            widget.destroy()

        #récupération des conversations
        self.chat, self.chat_user = self.charger_conv("chat.csv")

        self.afficher_chat()

    def afficher_new_conv(self):
        """
            Ouvre une nouvelle fenêtre permettant d'envoyer des messages à un nouvel utilisateur.

            Transmet l'utilisateur courant à la fenêtre Conversation.

            Vérifications effectuées :
                - l'utilisateur sélectionné existe dans la base de données.

            Si les données sont valides :
                - une nouvelle fenêtre de conversation s'ouvre
        """
        user2 = self.entry_user.get()
        conv = self.chat_user.get(user2,"")
        new_window = ctk.CTkToplevel(self)
        new_window.title(user2)
        new_window.geometry("500x425")

        Conversation(new_window, self.master.current_user, user2, conv)

        #else:
            #print("Erreur : Cet utilisateur n'est pas connu")


    def chercher_user(self, nom_recherche):
        """
            Recherche les aliments contenant le texte saisi
            par l'utilisateur -> utilisée dans Ajout

            Paramètre:
                - nom_recherche (str) : texte recherché.

            Retourne:
                - list : liste des aliments correspondants.
        """
        nom_recherche = nom_recherche.lower()

        resultats = [ nom for nom in self.users.keys() if nom_recherche in nom.lower()]

        return resultats

    # Pour le menu déroulant
    def update_suggestions(self, event):
        """
            Met à jour la liste des suggestions d'utilisateurs
            pendant la saisie dans le champ texte.

            Les suggestions proviennent de la méthode
            Aliment.chercher_aliment().

            Paramètre:
                - event : événement clavier déclenché lors de la saisie.
        """
        texte = self.entry_user.get().lower()

        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        suggestions = self.chercher_user(texte)
        if texte == "":
            suggestions = list(self.users.keys())

        if not suggestions:
            self.suggestion_frame.grid_remove()
            return

        self.suggestion_frame.grid(row=1,column=0,padx=40,sticky="ew")

        for user in suggestions[:4]:
            button = ctk.CTkButton(self.suggestion_frame,text=user,anchor="w",fg_color="transparent",hover_color=("gray80", "gray25"),command=lambda u=user: self.select_suggestion(u))
            button.pack(fill="x", padx=5, pady=2)


    def select_suggestion(self, user):
        """
            Insère le nom de l'utilisateur sélectionné dans le champ de saisie
            puis masque la liste des suggestions.

            Paramètre:
                - user (str) : l'utilisateur choisi par l'utilisateur courant.
        """

        self.entry_user.delete(0, "end")
        self.entry_user.insert(0, user)
        self.suggestion_frame.grid_remove()