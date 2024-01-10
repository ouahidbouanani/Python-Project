from TD4_FichierPrincipal import id2doc, id2aut
import pandas as pd
from Document import Document
from Author import Author
############################### "Q4.1" ###########################
class Corpus:
    _instance = None
    def __new__(cls, nom):
        if not cls._instance:
            cls._instance = super(Corpus, cls).__new__(cls)
            cls._instance.nom = nom
            cls._instance.authors = id2aut
            cls._instance.id2doc = id2doc
            cls._instance.ndoc = len(cls._instance.id2doc)
            cls._instance.naut = len(cls._instance.authors)
        return cls._instance

    def Add(self, doc): 
        if doc.auteur not in self.authors:
            self.naut += 1
            self.authors[doc.auteur] = Author(doc.auteur)
            self.authors[doc.auteur].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc 
    ######## Q3.2 ################
    def display_sorted_documents(self,num_documents,tri):
        if tri== 'titre':
          sorted_docs = list(sorted(self.id2doc.values(), key=lambda doc: doc.titre.lower()))[:num_documents]
          print("\n".join(list(map(repr, sorted_docs))))  
        elif tri== 'date':
          sorted_docs = list(sorted(self.id2doc.values(), key=lambda doc: doc.date))[:num_documents]
          print("\n".join(list(map(repr, sorted_docs))))  
        else:
          raise ValueError("Invalid value for tri parameter. Should be either 'titre' or 'date'")
    
    def __repr__(self):
        docs = list(self.id2doc.values())
        return "\n".join(list(map(str, docs)))

    def save(self):
        df = pd.DataFrame({
            'titre': [doc.titre for doc in self.id2doc.values()],
            'auteur': [doc.auteur for doc in self.id2doc.values()],
            'date': [doc.date for doc in self.id2doc.values()],
            'url': [doc.url for doc in self.id2doc.values()],
            'texte': [doc.texte for doc in self.id2doc.values()],
        })
        df.to_csv('DataCorpus.csv', index=False, sep='\t')

    def load(self):
        df = pd.read_csv('DataCorpus.csv', sep='\t',index_col=False)

        for index, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], row['date'], row['url'], row['texte'])
            self.Add(doc)


# Test du singleton
corpus1 = Corpus("Corpus 1")
corpus2 = Corpus("Corpus 2")

print(corpus1 is corpus2)  # Les deux variables pointent vers la même instance, car c'est un singleton
