from Aliment import Aliment
from menu import Menu
from Inventaire import Inventaire
from datetime import datetime, timedelta

#on teste la recherche d'aliments
class MockMaster: 
    def __init__(self):
        self.current_user = "Clémentine"


Aliment.base_aliments = {
    "pomme": {"calories": 52, "proteines": 0.3},
    "poire": {"calories": 57, "proteines": 0.4},
    "pain": {"calories": 120, "proteines": 6.0}
}

print("test de la recherche d'aliments")

#1. on teste s'il reconnait la sous chaine "po"

valeur_attendue_1 = ["pomme", "poire"]
if Aliment.chercher_aliment("po") == valeur_attendue_1:
    print(True)
else:
    print(False)

#2. on teste si il prend en compte les majuscules

valeur_attendue_2 = ["pain"]
if Aliment.chercher_aliment("PaiN") == valeur_attendue_2:
    print(True)
else:
    print(False)

##on teste les notifications d'alertes péremption

print("test du calcul des rappels de péremption")

#on crée les dates testes
aujourdhui = datetime.today()

aujourdhui_str = aujourdhui.strftime("%d/%m/%Y")
exp_3_jours = (aujourdhui + timedelta(3)).strftime("%d/%m/%Y")
exp_10_jours = (aujourdhui + timedelta(10)).strftime("%d/%m/%Y")


#on crée une fausse chaîne d'inventaire comme celle du CSV

fausse_chaine_inventaire = f"pomme:2:{aujourdhui_str}|fraise:1:{exp_3_jours}|beurre:1:{exp_10_jours}"

#on créé un menu simulé
master_mock = MockMaster()
menu_test = Menu.__new__(Menu) # crée l'objet sans lancer l'interface
menu_test.master = master_mock

# on simule un inventaire utilisateur : 
# La pomme expire aujourd'hui (0 jour), la fraise dans 3 jours, le beurre dans 10 jours (pas d'alerte)
menu_test.users = {
    "Clémentine": {
        "inventaire": f"pomme:2:{aujourdhui_str}|fraise:1:{exp_3_jours}|beurre:1:{exp_10_jours}"
    }
}

valeur_attendue_rappels = [
    "pomme expire dans 0 jours",
    "fraise expire dans 3 jours"
]

if menu_test.rappels() == valeur_attendue_rappels:
    print(True)
else:
    print(False)



##test découpage de la chaîne d'inventaire : le parsing

print("Test du découpage de la chaîne d'inventaire CSV")

inventaire_test = Inventaire.__new__(Inventaire)
chaine_brute_csv = "beurre:2:12/06/2026|salade:1:28/05/2026"

valeur_attendue_decoupe = [
    {"nom": "beurre", "quantite": "2", "date": "12/06/2026"},
    {"nom": "salade", "quantite": "1", "date": "28/05/2026"}
]

if inventaire_test.parser_inventaire(chaine_brute_csv) == valeur_attendue_decoupe:
    print(True)
else:
    print(False)


# test limite, recherche d'un aliment inexistant (Aliment.py)

print("Test aliment introuvable")

#si l'utilisateur tape n'importe quoi (ex: "xyz"), l'algo doit renvoyer une liste vide []
valeur_attendue_vide = []
if Aliment.chercher_aliment("xyz") == valeur_attendue_vide:
    print(True)
else:
    print(False)


# test rappels de péremption si l'inventaire est vide (menu.py)

print("test des rappels (cas inventaire vide)")

#si un utilisateur n'a aucun aliment dans son inventaire 
chaine_vide = ""

valeur_attendue_pas_d_alerte = []



