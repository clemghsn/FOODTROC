import csv

class Aliment():

    def charger_donnees(fichier_csv):
        dictionnaire_aliments = {} # dico aliments ou inventaire
        
        with open(fichier_csv, mode='r', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            
            for ligne in lecteur:
                nutriments = dict()
                nom = ligne['name'].lower() # On prend le nom et les calories lower = on s'est fou minuscules ou majuscules
                calories = ligne['calories']
                proteines = ligne['protein']
                nutriments['calories'] = calories
                nutriments['proteines'] = proteines
                
                dictionnaire_aliments[nom] = nutriments # On ajoute dans le dico
                
        return dictionnaire_aliments
    
    base_aliments = charger_donnees('nutrition.csv')

    def chercher_aliment(nom_recherche):
        nom_recherche = nom_recherche.lower()

        resultats = [ nom for nom in Aliment.base_aliments.keys() if nom_recherche in nom]

        return resultats

