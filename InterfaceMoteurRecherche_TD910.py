##### Importation des librairies nécessaires
import streamlit as st
import re
import json
from Corpus import Corpus
import numpy as np
############################# Configuration de la page
st.set_page_config(
    page_title="Moteur de recherche",
    page_icon="research.png",  
)
created=False
############# Définition des fonctions qu'on va utiliser
############ Prendre le vocabulaire et les documents qu'on a par l'appelle une instance de la classe corpus et la fonction concernée
Test=Corpus('TestValidation')
vocabulaire= Test.construire_vocabulaire()
documents=Test.id2doc
##### Fonction pour charger le dictionnaire (vectorisation des documents)
def loadVectorDicFromJson(file_path='DocVector.json'):
    try:
        with open(file_path, 'r') as json_file:
            vector_dic = json.load(json_file)
        return vector_dic
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return None
####### Fonction pour vectoriser l'entrée de l'utilisateur
def vectorizeEntry(userEntry):
    ##Initialisation des listes de vectorisation
    vectorList=[0]*len(vocabulaire)
    # boucle pour mettre les valeurs 1 pour les mots clefs d'utlisateur qui font la partie de vocabulaire
    for index,VocabWord in enumerate(list(vocabulaire)):
      if VocabWord in userEntry:
        vectorList[index]=1
      else:
        continue
    return vectorList
####### Function to calculate similarity by using Cosine similarity Cosine Similarity=(A⋅B)/(∥A∥⋅∥B∥)​
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity
####### Fonction pour retourner le top document au niveau de la similarité avec l'entrée ou la requete d'utilisateur
def TopMatchedDocument(vectorizedDocs,userEntryVectorized):
    similarities_results=[]
    # calculation des scores de similarité cosinus for tous les documents vectorisés avec requete d'utilisateur vectorisée
    for documentId in vectorizedDocs:
        IdentifiantDocument,similarityScore=documentId,round(cosine_similarity(userEntryVectorized,vectorizedDocs[documentId]),2)
        similarities_results.append((IdentifiantDocument,similarityScore))
    # retourner le top document en basant sur la similarité (on retourne identifiant de top document, score de similarité)
    similarities_results.sort(key=lambda x: x[1],reverse=True) # ordre decroissant par la score de similarité
    return  similarities_results[0]

##################### Creation les elements de la page
st.title("Recherche de Document")
# Get user input 
user_input = st.text_input("Entrez quelques mots-clés ou une requête représentant la description")
if st.button("Rechercher"):
# nettoyer la requete d'utlisateur par la suppression des nombres, ponctuations, caracteres speciaux
 cleaned_input = re.sub(r'[^a-zA-Z\s]', '', user_input.lower())
# Créer une liste contient les mots de requete d'utilisateur comme des elements de la liste sans duplication
 tokens=list(set(cleaned_input.split()))
########### Vectorisation de requete (entrée de l'utilisateur) 
 VectorizedEntry=vectorizeEntry(tokens)
### charger le dictionnaire de vectorisation des documents
 documents_vectors=loadVectorDicFromJson()
######## Afficher les tops documents similaires par rapport l'entrée de l'utilisateur
 topDocument=TopMatchedDocument(documents_vectors,VectorizedEntry)
# Affichage du TopDocument 
 chosen_doc_ID = topDocument[0] 
 document_info = f"**DocumentID:** {chosen_doc_ID}\n" \
                 f"**Titre:** {documents[chosen_doc_ID].titre}\n" \
                 f"**Auteur:** {documents[chosen_doc_ID].auteur}\n" \
                 f"**URL:** {documents[chosen_doc_ID].url}\n" \
                 f"**SimilarityScore:** {topDocument[1]}\n" \
                 f"**Origine:** {re.sub(r'[^a-zA-Z]', '', chosen_doc_ID)}\n" \
                 "\n\t"\
                 "**Contenu du document/ Description:**\n" \
                 f"{documents[chosen_doc_ID].texte}" 
# Affichage du document choisi
 st.markdown(f"### Document Information\n{document_info}", unsafe_allow_html=True)
 
