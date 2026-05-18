import folium
import os
import webbrowser
import csv


class Carte:

    def __init__(self):

        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=13)
        self.users = self.charger_donnees("users.csv")
        self.ajouter_markers()

    def charger_donnees(self, fichier_csv):

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

                icon=folium.Icon(color="green")

            ).add_to(self.carte)

    def format_aliments(self, aliments_string):

        aliments = aliments_string.split("|")

        noms = [
            aliment.split(":")[0].capitalize()
            for aliment in aliments
        ]

        return " • ".join(noms)

    def generer(self):

        file_path = os.path.abspath("map.html")

        self.carte.save(file_path)

        webbrowser.open(f"file://{file_path}")