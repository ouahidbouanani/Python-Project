########## Importation des librairie nécessaires ###########
import pandas as pd
import json
############ Q_2.3 ###########
# code pour importation des données
corpusData=pd.read_csv('Data.csv',sep='\t',index_col=False)
########################## Partie 3 : premières manipulation des données ########################################

############ Q_3.1: Nombre de documents. ###########
print(f'Nombre de documents: {corpusData.shape[0]}\n')
############ Q_3.2 : Nombre des phrases et des mots pour chaque document/ descriptive statistic  ###########
nb_phrases = [len(str(doc).split(".")) for doc in list(corpusData['Content'])]
nb_mots = [len(str(doc).split()) for doc in list(corpusData['Content'])]
df_info={'Document_Id':list(corpusData.Id),'Nb_Phrases':nb_phrases,'Nb_Mots':nb_mots}
df_info=pd.DataFrame(df_info)
print(df_info)
print(df_info.describe())
############ Q_3.3 : Supprimez les documents qui contiennent moins de 20 caractères #############

# prendre les documents qui ont plus 20 caractères
corpus = corpusData[corpusData['Content'].str.len() >= 20]
# Importer le jeu de donnée nettoyé
# Obtenir les indices des lignes qui satisfont les conditions : Content a moins que 20 caractères ou la présence des valeurs manquantes 
indices_documents_manquants = set(corpusData[corpusData['Content'].isna()].index)
indices_short_content = set(corpusData[corpusData['Content'].str.len() < 20].index)
indicesOfObservationsWillBeDeleted = list(indices_documents_manquants | indices_short_content) # combiner les indices des observation satisfont les conditions, depuis conversion set to liste
print(f' Number of deleted observations: {len(indicesOfObservationsWillBeDeleted)}')

corpusData=corpusData.loc[~corpusData.index.isin(indicesOfObservationsWillBeDeleted)]
corpusData.to_csv('Data_Cleaned.csv', sep='\t', index=False)
# Modifier les metadonnées par suppression les elements qui correspondent les indices d'observations à supprimer
file_path = 'metadata_listes.json'
with open(file_path, 'r') as json_file:
    metadata = json.load(json_file)

for metadataElement in metadata:
    metadata[metadataElement] = [element for idx, element in enumerate(metadata[metadataElement]) if idx not in indicesOfObservationsWillBeDeleted]
# Write the modified metadata back to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(metadata, json_file, indent=2)

############ Q_3.4 : Joint les documents en seule chaine caractères #############
joined_documents = ' '.join(corpus['Content'].astype(str))
# Affichage la chaine de caractères
print(joined_documents)
