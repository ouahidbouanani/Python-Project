################# Partie 2 :  classe : Author #################

############ Q_2.1: création de la classe Author ###########
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
       
    ### Q_2.2: méthode qui affiche toutes les informations d’une instance de la classe Author
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"NomAutheur: {self.name}\nNombreDocuments: {self.ndoc}\nProductions: {self.production}\n"
