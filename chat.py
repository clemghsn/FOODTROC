import customtkinter as ctk
from aliment import Aliment
from inventaire import Inventaire
import csv
from datetime import datetime

class Chat(ctk.CTkFrame):
    """
        Fenêtre permettant à un utilisateur d'envoyer des messages
        à d'autres utilisateurs.

        Cette interface contient :
            - un champ de saisie du nom de l'aliment,
            - un champ de quantité,
            - un champ de date de péremption,
            - ,
            - un bouton d'ajout dans le fichier users.csv.
    """

    def __init__(self, master, current_user):
        """
            Initialise la fenêtre de messagerie.

            Paramètres:
                - master : fenêtre
                - current_user (str) : identifiant de l'utilisateur connecté.
        """
        super().__init__(master)
        self.current_user = current_user
        self.pack(fill="both", expand=True)

        #récupération des conversations
        self.chat = self.charger_conv("chat.csv")
        

        # centrer le contenu
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # carte centrale 
        self.card = ctk.CTkFrame(self, corner_radius=15, width=320, height=350)
        self.card.grid(row=0, column=0)
        self.card.grid_propagate(False)


        self.card.grid_columnconfigure(0, weight=1)


        self.title = ctk.CTkLabel(self.card,text="Messagerie",font=ctk.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, pady=(20, 5))

        # Conversations
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nsew",padx=25, pady=10)
        self.afficher_chat()

        self.label_new = ctk.CTkLabel(self.card,text="Nouvelle conversation",font=("Arial", 14, "bold"))
        self.label_new.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Entrée
        self.entry_aliment = ctk.CTkEntry(self.card,placeholder_text="Recherche utilisateur",height=40)
        self.entry_aliment.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

        # détecter quand on tape
        self.entry_aliment.bind("<KeyRelease>", self.update_suggestions)

        self.suggestion_frame = ctk.CTkFrame(self.card,corner_radius=10,border_width=1)

        # Bouton nouvelle conv
        self.button_new = ctk.CTkButton(self.card,text="Ecrire",height=45,corner_radius=10,command=self.afficher_new_conv)
        self.button_new.grid(row=5, column=0, padx=40, pady=(20, 20), sticky="ew")

    def charger_conv(self, fichier_csv):
        """
            Charge les conversations des utilisateurs depuis un fichier CSV.

            Les informations récupérées sont :
                - l'inventaire
                - les aliments postés

            Paramètre:
                - fichier_csv (str) : chemin du fichier CSV.

            Retourne:
                - users (dict) : dictionnaire contenant les données utilisateurs.
        """

        conv = {}

        with open(fichier_csv, mode='r', encoding='utf-8') as f:

            lecteur = csv.DictReader(f)


            for ligne in lecteur:
                print(ligne)

                if ligne["sender"] == self.current_user:
                    message = conv.get(ligne["receiver"],"")
                    message += ":envoyé"
                    conv[ligne["receiver"]] = {"messages" : message}
                    
                elif ligne["receiver"] == self.current_user:
                    message = conv.get(ligne["sender"],"")
                    message += ":recu"
                    conv[ligne["sender"]] = {"messages" : message}
            

        return conv
    
    def afficher_chat(self):
        """
            Affiche tous les conversations de l'utilisateur.
        """
        for user2 in self.chat.keys():
            self.create_card(user2)

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

        button_ouvrir = ctk.CTkButton(card,text="Ouvrir",font=("Arial", 16, "bold"), width=3, corner_radius=15, fg_color = "grey", command=lambda a=user2: self.afficher_conv(a))
        button_ouvrir.grid(row=0, column=1, padx=(0, 5), pady=5)
    
        button_supprimer = ctk.CTkButton(card,text="Supprimer",font=("Arial", 16, "bold"), width=3, corner_radius=15, fg_color = "grey", command=lambda a=user2: self.suppr_conv(a))
        button_supprimer.grid(row=0, column=2, padx=(0, 5), pady=5)

    def afficher_conv(self, user2):
        """
            Ouvre une nouvelle fenêtre permettant d'envoyer des messages aux autres utilisateurs.

            Transmet l'utilisateur courant à la fenêtre Conversation.
            """
        new_window = ctk.CTkToplevel(self)
        new_window.title(user2)
        new_window.geometry("320x350")
        Ajout(new_window, self.master.current_user)

    def suppr_conv(self, user2):
        """
            Supprime la conversation avec l'utilisateur user2 dans le fichier chat.csv
            """

    def afficher_new_conv(self):
        """
            Ouvre une nouvelle fenêtre permettant d'envoyer des messages à un nouvel utilisateur.

            Transmet l'utilisateur courant à la fenêtre Conversation.

            Vérifications effectuées :
                - l'utilisateur sélectionné existe dans la base de données.

            Si les données sont valides :
                - une nouvelle fenêtre de conversation s'ouvre
        """
        aliment = self.entry_aliment.get()
        quantite = self.entry_quantite.get()
        date = self.entry_date.get()

            
        if isinstance(self.master, ctk.CTkToplevel): # ferme la fenêtre de saisie après l'ajout
                self.master.destroy()
        else:
            print("Erreur : Cet utilisateur n'est pas connu")

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