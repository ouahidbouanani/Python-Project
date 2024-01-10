from abc import ABC, abstractmethod

####################################### "Q4.2" ###################################################

# Classe de base pour les documents
class Document(ABC):
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    @abstractmethod
    def getType(self):
        pass

# Sous-classe RedditDocument
class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_commentaires):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_commentaires = nb_commentaires

    def getType(self):
        return "Reddit"

# Sous-classe ArxivDocument
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs

    def getType(self):
        return "Arxiv"

# Usine (Factory) pour créer des instances de Document
class DocumentFactory:
    def create_document(self, document_type, **kwargs):
        if document_type == "Reddit":
            return RedditDocument(**kwargs)
        elif document_type == "Arxiv":
            return ArxivDocument(**kwargs)
        else:
            raise ValueError("Invalid document type")

# Validation de la classe factory
factory = DocumentFactory()

reddit_doc = factory.create_document("Reddit", titre="Titre Reddit", auteur="Auteur Reddit", date="2024-01-08", url="http://reddit.com", texte="Contenu du message Reddit", nb_commentaires=100)
arxiv_doc = factory.create_document("Arxiv", titre="Titre Arxiv", auteur="Auteur Principal", date="2024-01-08", url="http://arxiv.org", texte="Contenu de l'article Arxiv", co_auteurs=["Co-Auteur1", "Co-Auteur2", "Co-Auteur3"])

print(reddit_doc.getType())  # Affiche "Reddit"
print(arxiv_doc.getType())   # Affiche "Arxiv"

################################" Partie 5: Voici le lien de google colab: https://colab.research.google.com/drive/10yNBMEO61r2ACgPhqpNfs2O3RUZdsUY4?usp=sharing " ####################