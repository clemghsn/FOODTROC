import folium
import os
import webbrowser
import csv


class Carte:
    """
        Classe permettant de générer une carte interactive Folium
        affichant les utilisateurs et leurs aliments postés.

        Chaque utilisateur est représenté par un marqueur contenant :
            - son nom
            - son adresse
            - son numéro de téléphone
            - ses aliments disponibles
    """

    def __init__(self):
        """
            Initialise la carte centrée sur Lyon, charge les données 
            des utilisateurs puis ajoute les marqueurs sur la carte.
        """
        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=13)
        self.users = self.charger_donnees("users.csv")
        self.ajouter_markers()

    def charger_donnees(self, fichier_csv):
        """
            Charge les données des utilisateurs depuis un fichier CSV.

            Les informations récupérées incluent :
                - l'identifiant utilisateur
                - le mot de passe
                - le téléphone
                - l'adresse
                - les coordonnées GPS
                - l'inventaire
                - les aliments postés

            Paramètre:
                - fichier_csv (str) : chemin du fichier CSV

            Retourne:
                - list : liste de dictionnaires contenant les données utilisateurs
        """
        users = []

        with open(fichier_csv, mode='r', encoding='utf-8') as f:

            lecteur = csv.DictReader(f)
            print(lecteur.fieldnames)

            for ligne in lecteur:

                user = {
                    "id_user": ligne["id_user"],
                    "password": ligne["password"],
                    "telephone": ligne["telephone"],
                    "adresse": ligne["adresse"],
                    "latitude": float(ligne["latitude"]),
                    "longitude": float(ligne["longitude"]),
                    "inventaire": ligne["inventaire"],
                    "aliments_postes": ligne["aliments_postes"]
                }

                users.append(user)

        return users

    def ajouter_markers(self):
        """
            Ajoute un marqueur pour chaque utilisateur
            présent dans la liste des utilisateurs.

            Chaque marqueur contient une popup affichant :
                - le nom de l'utilisateur,
                - son adresse,
                - son téléphone,
                - les aliments postés.
        """
        for user in self.users:

            popup_html = f"""
            <div style="
                font-family: Arial;
                font-size: 13px;
                min-width: 180px;
                white-space: nowrap;
            ">
                <b style="font-size:14px;">
                    {user['id_user']}
                </b><br>

                📍 {user['adresse']}<br>

                📞 {user['telephone']}<br>

                🍽️ {self.format_aliments(user['aliments_postes'])}
            </div>
            """

            folium.Marker(

                location=[
                    user["latitude"],
                    user["longitude"]
                ],

                popup=folium.Popup(
                    popup_html,
                    max_width=300
                ),

                tooltip=user["id_user"],

                icon=folium.Icon(color="green", icon="cutlery", prefix="fa")

            ).add_to(self.carte)

    def format_aliments(self, aliments_str):
        """
            Formate la chaîne des aliments postés afin d'afficher 
            uniquement leurs noms.

            Les aliments sont séparés par des puces.

            Paramètre:
                - aliments_str (str) : chaîne contenant les aliments

            Retourne:
                - str : noms des aliments formatés
        """
        aliments = aliments_str.split("|")

        noms = [
            aliment.split(":")[0].capitalize()
            for aliment in aliments
        ]

        return " • ".join(noms)

    def generer(self):
        """
            Génère le fichier HTML de la carte
            puis l'ouvre automatiquement dans le navigateur web.
        """
        file_path = os.path.abspath("map.html")

        self.carte.save(file_path)

        webbrowser.open(f"file://{file_path}")