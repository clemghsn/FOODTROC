import csv

class Aliment():
    """
    Classe permettant de charger et rechercher des aliments
    à partir du fichier nutrition.csv.

    Les aliments sont stockés dans un dictionnaire contenant
    leurs informations nutritionnelles principales
    (calories et protéines).
    """

    def charger_donnees(fichier_csv):
        """
            Charge les données nutritionnelles depuis un fichier CSV
            et les stocke dans un dictionnaire.

            Chaque aliment est associé à :
                - son nombre de calories,
                - sa quantité de protéines.

            Paramètres:
                - fichier_csv (str) : chemin du fichier CSV contenant
                les données nutritionnelles.

            Retourne:
                - dict : dictionnaire des aliments et de leurs nutriments.
        """
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
    
    # dictionnaire contenant tous les aliments de nutrition.csv
    base_aliments = charger_donnees('nutrition.csv')

    def chercher_aliment(nom_recherche):
        """
            Recherche les aliments contenant le texte saisi
            par l'utilisateur -> utilisée dans Ajout

            Paramètre:
                - nom_recherche (str) : texte recherché.

            Retourne:
                - list : liste des aliments correspondants.
    """
        nom_recherche = nom_recherche.lower()

        resultats = [ nom for nom in Aliment.base_aliments.keys() if nom_recherche in nom]

        return resultats

