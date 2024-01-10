from Document import Document
from Author import Author
import pandas as pd
import json
######################### TD:4-Partie:1-Q_1.3 ################################
# Lecture de l'ensemble de listes depuis le fichier JSON
with open('metadata_listes.json', 'r') as fichier_json:
    metadata_lu = json.load(fichier_json)
# importer le jeu de donnée crée en TD3 pour extraire les clefs (identifiants des documents)
corpusData=pd.read_csv('Data_Cleaned.csv',sep='\t',index_col=False)
# valider qu'on a meme nombre de documents (observations) dans les listes de metadonnées et la liste des Ids
clefs= list(corpusData['Id']) 
assert(len(metadata_lu["titles"]),len(metadata_lu["authors"]),len(metadata_lu["Publiction_dates"]),len(metadata_lu["links"]), len(metadata_lu["documents"]),len(clefs))

# Création des instances de la classe Document
documents_instance = [
    Document(titre, auteur, date, url, texte)
    for titre, auteur, date, url, texte in zip(
        metadata_lu["titles"], metadata_lu["authors"], metadata_lu["Publiction_dates"],metadata_lu["links"], metadata_lu["documents"]
    )
]
##### Creation de la dictionnaire ou collection id2doc par l'usage de la liste des instances Document et Clefs, key=clefs, value=instanceDocument
id2doc = dict(zip(clefs, documents_instance))

####### Partie 2-Q2.3: Création dictionnaire id2aut #############
id2aut={}
## vérification l'existence d'un auteur dans la dictionnaire id2auth avant de l'ajouter
for doc in id2doc:
    if id2doc[doc].auteur in id2aut:
        pass
    else:
        auteur=Author(id2doc[doc].auteur)
        id2aut[doc]=auteur

