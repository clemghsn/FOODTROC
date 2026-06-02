import customtkinter as ctk
import csv
from PIL import Image
from datetime import datetime

class Conversation(ctk.CTkFrame):
    """
        Fenêtre permettant à un utilisateur d'envoyer des messages
        à d'autres utilisateurs.

        Cette interface contient :
            - un scroll text affichant les messages échangés,
            - un champ de saisie pour écrire un nouveau message,
            - un bouton pour envoyer le messages.
    """

    def __init__(self, master, current_user, user2, conv):
        """
            Initialise la fenêtre de conversation.

            Paramètres:
                - master : fenêtre
                - current_user (str) : identifiant de l'utilisateur connecté
                - user2(str) : nom de l'interlocuteur
                - conv(str) : conversation entre les 2 utilisateurs.
        """
        super().__init__(master)
        self.current_user = current_user
        self.user2 = user2
        self.conv = conv
        self.pack(fill="both", expand=True)

        #récupération des conversations
        self.messages = self.charger_conv(self.conv)

        #images
        self.img_send = ctk.CTkImage(light_image=Image.open("images/send.png"), size=(20, 20))

        # centrer le contenu
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # carte centrale 
        self.card = ctk.CTkFrame(self, corner_radius=15, width=300, height=50)
        self.card.grid(row=0, column=0, columnspan = 3)
        self.card.grid_propagate(False)

        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(0, weight=1)


        self.title = ctk.CTkLabel(self.card,text=user2,font=ctk.CTkFont(size=14, weight="bold"))
        self.title.grid(row=0, column=0, pady=10)



        # Conversations
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, columnspan = 3, sticky="nsew",padx=30, pady=10)
        self.afficher_chat()

        # carte nouveau message
        self.card2 = ctk.CTkFrame(self, corner_radius=15, width=300, height=50)
        self.card2.grid(row=3, column=0, columnspan = 3)
        self.card2.grid_propagate(False)

        self.card2.grid_columnconfigure(0, weight=1)
        self.card2.grid_columnconfigure(1, weight=1)
        self.card2.grid_columnconfigure(2, weight=2)
        #self.card2.grid_columnconfigure(2, weight=2)

        # Entrée
        self.entry_text = ctk.CTkEntry(self.card2,placeholder_text="Nouveau message",height=20)
        self.entry_text.grid(row=0, column=0, columnspan=2, padx=20, pady=30)

        # Bouton envoi
        self.button_send = ctk.CTkButton(self.card2,text="",image = self.img_send, height=45,corner_radius=10, fg_color = "transparent", command=self.enregister_message)
        self.button_send.grid(row=0, column=2, padx=20, pady=20)

    def charger_conv(self, conv):
        """
            Charge la conversation des utilisateurs extraite du fichier chat.csv.

            Les informations récupérées sont :
                - le message
                - la date d'envoi
                - l'heure d'envoi
                - l'état du message (envoyé ou reçu)

            Paramètre:
                - conv (str) : suite de messages.

            Retourne:
                - l_messages (list) : liste contenant les messages.
        """

        l_messages = []
        print(conv)
        conv = conv.split("|") if conv else []
        for message in conv :
            message = message.split(":")
            print(message)
            if message != [] and message != ['']:
                print(message)
                text = message[0]
                date = message[1]
                heure = message[2]
                etat = message[3]
                ligne = {"text":text, "date":date, "heure":heure, "etat" : etat}
                l_messages.append(ligne)

        return l_messages
    
    def afficher_chat(self):
        """
            Affiche mes messages.
        """
        for message in self.messages:
            self.create_card(message)

    def create_card(self, message):
        """
            Crée une carte représentant un message.

            La carte affiche :
                - la date d'envoi
                - l'heure d'envoi
                - le contenu du message
               
            Paramètres:
                message (dict) : dictionnaire contenant
                les informations du message.
        """

        card = ctk.CTkFrame(self.scroll, corner_radius=10)
        if message["etat"] == "reçu":
            card.pack(padx=10, pady=5, side = "left")
        else :
            card.pack(padx=10, pady=5, side = "right")

        # colonne extensible
        card.grid_columnconfigure(3, weight=1)

        label_date = ctk.CTkLabel(card,text=message["date"],font=("Arial", 10, "bold"))
        label_date.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label_heure = ctk.CTkLabel(card,text=message["heure"],font=("Arial", 10, "bold"))
        label_heure.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        label_heure = ctk.CTkLabel(card,text=message["text"],font=("Arial", 14, "bold"))
        label_heure.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    
    def enregister_message(self):
        """
            Ajoute un message dans le chat.

            Paramètres:
                - nom (str) : nom de l'aliment.
                - qte (int ou str) : quantité de l'aliment.
                - date (str) : date de péremption au format JJ/MM/AAAA.
        """
        fichier = 'chat.csv'
        messages = []

        with open(fichier, mode='r', newline='', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            colonnes = lecteur.fieldnames  

            for ligne in lecteur:
                messages.append(ligne)

        #nouveau message
        message = self.entry_text.get()
        date = datetime.today().date()
        time = str(datetime.today().time()).split(":")
        heure = f"{time[0]}h{time[1]}"
        text = f"{message}:{date}:{heure}"
        new_mess = {"sender":self.current_user,"receiver":self.user2,"messages":text}
        messages.append(new_mess)

        with open(fichier, mode='w', newline='', encoding='utf-8') as f:

            writer = csv.DictWriter(f, fieldnames=colonnes)
            writer.writeheader()
            for mess in messages:
                writer.writerow(mess)

        print(f"{self.current_user} a envoyé un message à {self.user2}")

        self.refresh()

    def refresh(self):
        """
            Recharge les données de la conversation puis met à jour
            l'affichage des cartes dans l'interface graphique.
        """
        for widget in self.scroll.winfo_children():
            widget.destroy()

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
            
    
        self.chat, self.chat_user = chat, conv
        conv = self.chat_user[self.user2]
        self.messages = self.charger_conv(conv)

        self.afficher_chat()
