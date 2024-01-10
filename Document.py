################# Partie 1 : première classe : le Document #################

############ Q_1.1: création de la classe Document ###########
class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def getType(self):
        pass
    ### Q_1.2: méthode qui affiche toutes les informations d’une instance de la classe Document
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    
    def __str__(self):
        return f"Titre: {self.titre}\nAuteur: {self.auteur}\nURL: {self.url}\n"
##################################################### TD5/Partie1: classe RedditDocument ####################################################
class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_commentaires):
        super().__init__(titre, auteur, date, url, texte)
        self.set_nb_commentaires(nb_commentaires)
    # Polymorphism or overriding for getType function
    def getType(self):
        return "Reddit"
    # Accesseur pour le nombre de commentaires
    def get_nb_commentaires(self):
        return self.__nb_commentaires

    # Mutateur pour le nombre de commentaires
    def set_nb_commentaires(self, nb_commentaires):
        self.__nb_commentaires = nb_commentaires

    # Méthode pour afficher les informations de l'objet
    def __str__(self):
        return f"{super().__str__()}Nombre de commentaires : {self.__nb_commentaires}\n"
##################################################### TD5/Partie2: classe classe ArxivDocument ####################################################
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.set_co_auteurs(co_auteurs)

    # Accesseur pour les co-auteurs
    def get_co_auteurs(self):
        return self.__co_auteurs

    # Mutateur pour les co-auteurs
    def set_co_auteurs(self, co_auteurs):
        self.__co_auteurs = co_auteurs
    
    # Polymorphism or overriding for getType function
    def getType(self):
        return "Arxiv"

    # Méthode pour afficher les informations de l'objet
    def __str__(self):
        return f"{super().__str__()}Co-auteurs : {', '.join(self.__co_auteurs)}\n"


# validation
# document_arxiv = ArxivDocument("Titre Arxiv", "AuteurArxif", "15-02-2023", "http://arxiv.org", "Contenu de l'article Arxiv", ["Auteur1", "Auteur2"])
# document_reddit = RedditDocument("Titre Reddit", "AuteurReddit", "15-02-2023", "http://reddit.com", "Contenu du poste Reddit", 2)
# print(document_reddit)
# print(document_arxiv)
#print(document_reddit.__nb_commentaires) # validate privacy of nb_commentaire attribute