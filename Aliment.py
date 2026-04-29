import csv

def charger_donnees(fichier_csv):
    dictionnaire_aliments = {} # dico aliments ou inventaire
    
    with open(fichier_csv, mode='r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        
        for ligne in lecteur:
            nom = ligne['name'].lower() # On prend le nom et les calories lower = on s'est fou minuscules ou majuscules
            calories = ligne['calories']
            
            dictionnaire_aliments[nom] = calories # On ajoute dans le dico
            
    return dictionnaire_aliments

base_aliments = charger_donnees('nutrition.csv')

def chercher_aliment(nom_recherche):
    nom_recherche = nom_recherche.lower()
    
    # teste si le mot est dans l'intitulé de l'aliment
    resultats = {nom: cal for nom, cal in base_aliments.items() if nom_recherche in nom}
    
    if resultats:
        print(f"Résultats pour '{nom_recherche}' ")
        # On affiche les 5 premiers résultats 
        for i, (nom, cal) in enumerate(resultats.items()): # enumerate transforme une liste ou dico en un couple (numéro, valeur)
            print(f"{nom} : {cal} calories")
            if i >= 4: 
                print("... (il y a d'autres résultats)")
                break
    else:
        print("Aliment non trouvé.")

# test
chercher_aliment("Chicken")

