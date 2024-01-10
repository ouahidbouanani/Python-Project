from Corpus import Corpus
import numpy as np
import json
############ Prendre le vocabulaire et les documents qu'on a par l'appelle une instance de la classe corpus et la fonction concernée
Test=Corpus('TestValidation')
vocabulaire= Test.construire_vocabulaire()
documents=Test.id2doc
# fonction pour vectoriser tous documents qu'on a
def vectorizationDoc():
  vector_dic={}
  for identifiant in documents:
     docVector=[0]*len(vocabulaire)
     document = documents[identifiant].texte
     document= document.split()
     for index,VocabWord in enumerate(list(vocabulaire)):
        if VocabWord in document:
            docVector[index]=1
        else:
            continue
     vector_dic[identifiant]=docVector
  # Save the dictionary to a JSON file
  with open('DocVector.json', 'w') as json_file:
      json.dump(vector_dic, json_file)

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

# appeler la fonction vectorizationDoc pour sauvegarder au disque dur le dictionnaire de vectorisation des documents
#vectorizationDoc()

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
####### Fonction pour retourner les tops documents au niveau de la similarité avec l'entrée ou la requete d'utilisateur
def TopMatchedDocuments(vectorizedDocs,userEntryVectorized):
    similarities_results=[]
    # calculation des scores de similarité cosinus for tous les documents vectorisés avec requete d'utilisateur vectorisée
    for documentId in vectorizedDocs:
        IdentifiantDocument,similarityScore=documentId,round(cosine_similarity(userEntryVectorized,vectorizedDocs[documentId]),2)
        similarities_results.append((IdentifiantDocument,similarityScore))
    # retourner les 3 tops documents en basant sur la similarité (on retiurne identifiants des tops documents, score de similarité)
    similarities_results.sort(key=lambda x: x[1],reverse=True) # ordre decroissant par la score de similarité
    return  similarities_results[:3]

########## Exécution des codes ########

########### Demande à l'utilisateur de saisir les mots clefs
requete_utilisateur = input("Entrez quelques mots-clés séparés par des espaces (ou une requete représente description), pour trouver le document ciblé : ").lower().split()
########### Vectorisation de requete (entrée de l'utilisateur) 
VectorizedEntry=vectorizeEntry(requete_utilisateur)
### charger le dictionnaire de vectorisation des documents
documents_vectors=loadVectorDicFromJson()
######## Afficher les tops documents similaires par rapport l'entrée de l'utilisateur
topDocuments=TopMatchedDocuments(documents_vectors,VectorizedEntry)
print("*************Voici les identifiants, les scores de similarité de top 3 documents:\n**********")
print(f"ID_Document: {topDocuments[0][0]} / SimilarityScore: {topDocuments[0][1]}")
print(f"ID_Document: {topDocuments[1][0]} / SimilarityScore: {topDocuments[1][1]}")
print(f"ID_Document: {topDocuments[2][0]} / SimilarityScore: {topDocuments[2][1]}")

#### demande à l'utilisateur de choisir le document
choixDocUtilisateur=input("Choose the document that you want, enter 1(document with high similarty score) or 2 or 3 :")
#### Affichage de le document choisi ###
if int(choixDocUtilisateur)==1:
  print(f"{documents[topDocuments[0][0]]} \n {documents[topDocuments[0][0]].texte}")
elif int(choixDocUtilisateur)==2:
  print(f"{documents[topDocuments[1][0]]} \n {documents[topDocuments[1][0]].texte}")
elif int(choixDocUtilisateur)==3:
  print(f"{documents[topDocuments[2][0]]} \n {documents[topDocuments[2][0]].texte}")
else:
  print("Please enter just 1 or 2 or 3!!")