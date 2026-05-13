import folium
import os
import webbrowser

class Carte:

    def __init__(self):
        self.carte = folium.Map(location=[45.75, 4.85], zoom_start=13)

        self.users = [
            {"nom": "Clémentine", "mdp": "1234", "adresse": "???", "tel": "07 66 25 77 35", "coords": [45.75, 4.85], "poste": "Lait"},
            {"nom": "Angélique", "mdp": "5678", "adresse": "???", "tel": "06 66 25 77 35", "coords": [45.76, 4.83], "poste": "Oeufs"},
            {"nom": "Claire", "mdp": "abcd", "adresse": "???", "tel": "07 14 25 77 35", "coords": [45.74, 4.87], "poste": "Tomates"},
            {"nom": "Héloïse", "mdp": "efgh", "adresse": "???", "tel": "06 86 68 03 43", "coords": [45.75, 4.87], "poste": "Fromage"}
        ]

        self.ajouter_markers()

    def ajouter_markers(self):
        for user in self.users:
            popup_html = f"""
            <div style="
                font-family: Arial;
                font-size: 13px;
                min-width: 120px;
                white-space: nowrap;
            ">
                <b style="font-size:14px;">{user['nom']}</b><br>
                📍 {user['adresse']}<br>
                📞 {user['tel']}<br>
                🍽️ {user['poste']}
            </div>
            """

            folium.Marker(
                location=user["coords"],  
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=user["poste"],
                icon=folium.Icon(color="green")
            ).add_to(self.carte)

    def generer(self):
        file_path = os.path.abspath("map.html")
        self.carte.save(file_path)
        webbrowser.open(f"file://{file_path}")