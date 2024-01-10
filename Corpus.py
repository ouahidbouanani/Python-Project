#################### TD4: Partie3 ###################
from TD4_FichierPrincipal import id2doc, id2aut
from Author import Author
import pandas as pd
from Document import Document
import re
from collections import defaultdict
from scipy.sparse import csr_matrix
import numpy as np
########### Q3.1: Création de la classe Corpus ###########
class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = id2aut
        self.id2doc = id2doc
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

    def Add(self, doc): # doc is an instance of Document classe
        if doc.auteur not in self.authors:
            self.naut += 1
            self.authors[doc.auteur] = Author(doc.auteur)
            self.authors[doc.auteur].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc # l'ajout de la nouvelle document avec assigner le nombre de document comme un identifiant ou un clé
    ######## Q3.2 ################
    def display_sorted_documents(self,num_documents,tri):
        # Trier par ordre ascendant les documents en basnt sur le paramètre tri, Affichage des documents triés en basant sur la méthode __repr__
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
    ############ Q3.3: save and load functions ############""
    def save(self):
        # Create a DataFrame from the documents
        df = pd.DataFrame({
            'titre': [doc.titre for doc in self.id2doc.values()],
            'auteur': [doc.auteur for doc in self.id2doc.values()],
            'date': [doc.date for doc in self.id2doc.values()],
            'url': [doc.url for doc in self.id2doc.values()],
            'texte': [doc.texte for doc in self.id2doc.values()],
        })

        # Save the DataFrame to a CSV file
        df.to_csv('DataCorpus.csv', index=False, sep='\t')

    def load(self):
        # Load the DataFrame from a CSV file
        df = pd.read_csv('DataCorpus.csv', sep='\t',index_col=False)
        # create joined document au place de l'emporter de fichier TD3_2.py
        self.joined_documents = ' '.join(df['texte'].astype(str))
        # Update the corpus with the loaded documents
        for index, row in df.iterrows():
            doc = Document(row['titre'], row['auteur'], row['date'], row['url'], row['texte'])
            self.Add(doc)
    ########## TD6: Partie1. Q1.1 ###########
    def search(self, mot_clef):
        # Utiliser une expression régulière pour rechercher le mot-clé dans la chaîne de caractères concaténée
        passages = re.findall(fr'\b{re.escape(mot_clef)}\b', self.joined_documents, flags=re.IGNORECASE)
        return passages
    ########## TD6: Partie1. Q1.2
    def concorde(self, expression, taille_contexte):

        # Utiliser une expression régulière pour rechercher l'expression dans la chaîne de caractères concaténée
        matches = re.finditer(fr'(?P<gauche>.{{0,{taille_contexte}}})\b{re.escape(expression)}\b(?P<droit>.{{0,{taille_contexte}}})', 
                              self.joined_documents, flags=re.IGNORECASE)

        # Stocker les résultats dans un tableau pandas
        concordance_data = {'contexte_gauche': [], 'motif_trouve': [], 'contexte_droit': []}
        for match in matches:
            concordance_data['contexte_gauche'].append(match.group('gauche'))
            concordance_data['motif_trouve'].append(match.group())
            concordance_data['contexte_droit'].append(match.group('droit'))
        # Retourner les résultats sous forme de DataFrame
        concordance_df = pd.DataFrame(concordance_data)
        return concordance_df
    ########## TD6: Partie2. Q2.1
    def nettoyer_texte(self,texte):
        # Mise en minuscules
        texte = texte.lower()
        # Remplacement des passages à la ligne
        texte = texte.replace('\n', ' ')
        # Remplacement des ponctuations et des chiffres, caractères speciaux par espace (carctère vide)
        texte = re.sub(r'[^a-z\s]', '', texte)
        return texte
    ########## TD6: Partie2. Q2.2
    def construire_vocabulaire(self):
        # Initialisez un ensemble vide pour stocker les mots uniques
        vocabulaire_set = set()
        # Boucle sur les documents du corpus
        for doc in self.id2doc.values():
            # Suppression des ponctuations, chiffres, caracteres speciaux
            doc.texte=self.nettoyer_texte(doc.texte)
            # Utilisez la fonction split pour diviser le texte en mots
            mots = re.split(r'\s+', doc.texte)
            # Ajoutez les mots à l'ensemble
            vocabulaire_set.update(mots)
        # Convertissez l'ensemble en un dictionnaire si nécessaire: (keys are words and values are nbr of occurences that are 1 (set))
        vocabulaire_dict = dict.fromkeys(vocabulaire_set, 1)
        return vocabulaire_dict
    ################ TD6: Partie2. Q2.3
    def construire_vocabulaire_et_calculer_occurrences(self):
        # Initialisez un dictionnaire pour stocker les occurrences de chaque mot
        occurrences = {}
        # Initialisez un ensemble vide pour stocker les mots uniques du vocabulaire
        vocabulaire_set = set()
        # Boucle sur les documents du corpus
        for doc in self.id2doc.values():
            # Suppression des ponctuations, chiffres, caracteres speciaux
            doc.texte=self.nettoyer_texte(doc.texte)
            # Utilisez la fonction split pour diviser le texte en mots
            mots = re.split(r'\s+', doc.texte)
            # Ajoutez les mots à l'ensemble du vocabulaire
            vocabulaire_set.update(mots)
            # Mettez à jour le dictionnaire des occurrences
            for mot in mots:
                occurrences[mot] = occurrences.get(mot, 0) + 1
        # Créez un DataFrame à partir du dictionnaire des occurrences
        freq = pd.DataFrame(list(occurrences.items()), columns=['Mot', 'Occurrences'])
        # Tri du DataFrame par ordre décroissant d'occurrences
        freq = freq.sort_values(by='Occurrences', ascending=False)
        # Ajoutez nouvelle colonne pour le nombre de documents contenant chaque mot
        freq['Document_Frequency'] = freq['Mot'].apply(lambda mot: self.calcule_document_frequency(mot))
        return freq
    ###### TD6. Partie2 Q2.4
    def calcule_document_frequency(self, mot):
        # Initialisez le compteur
        document_count = 0
        # Parcourez les documents pour compter le nombre de documents contenant le mot
        for doc in self.id2doc.values():
            if mot in doc.texte:
                document_count+= 1
        return document_count
    #################### TD7: Partie1: matrice Documents x Mots ########################
    ######### Q1.1
    def construire_vocab_informations(self):
        # Construire le vocabulaire à partir des documents du corpus
        vocabulaire_set = self.construire_vocabulaire()
        # Trier le vocabulaire par ordre alphabétique
        vocabulaire = sorted(list(vocabulaire_set))
        # Initialiser le dictionnaire vocab
        vocab = defaultdict(dict)
        # Remplir le dictionnaire vocab avec des informations sur chaque mot
        for idx, mot in enumerate(vocabulaire):
            # Ajouter l'identifiant unique et le nombre total d'occurrences
            vocab[mot]['Identifiant'] = idx   # L'index commence à 0
            vocab[mot]['Occurences'] = self.calcule_occurrences(mot)
            # Ajouter d'autres informations si nécessaire
        return vocab
    
    def calcule_occurrences(self, mot):
        # Calcule le nombre total d'occurrences du mot dans l'ensemble des documents
        occurrences_totales = sum([doc.texte.lower().split().count(mot) for doc in self.id2doc.values()])
        return occurrences_totales
    ######### Q1.2 
    def construire_matrice_tf(self,vocab):
        # Initialiser les listes pour les indices de ligne, de colonne et les valeurs de la matrice
        indices_ligne = []
        indices_colonne = []
        valeurs = []
        docidx=-1
        # Parcourir chaque document du corpus
        for doc_id, doc in self.id2doc.items():
            # Parcourir chaque mot dans le vocabulaire
            docidx+=1
            print(f"Progress: {round(docidx*100/len(self.id2doc),2)}%") #Cet affichage a pour but de déterminer l'avancement d'execution du code 
            for mot in vocab:
                # Récupérer l'identifiant unique du mot dans le vocabulaire
                mot_id = vocab[mot]['Identifiant']
                # Récupérer le nombre d'occurrences du mot dans le texte du document
                occurrences_mot = doc.texte.lower().split().count(mot)
                # Ajouter les indices et la valeur à les listes correspondantes
                indices_ligne.append(docidx)  # L'index commence à 0
                indices_colonne.append(mot_id)  # L'index commence à 0
                valeurs.append(occurrences_mot)
        # Construire la matrice CSR à partir des listes
        mat_tf = csr_matrix((valeurs, (indices_ligne, indices_colonne)), shape=(self.ndoc, len(vocab)))
        mat_tf=mat_tf.toarray()
        return mat_tf
    ####### Q1.3
    def modification_vocab_calcul(self,vocab):
        """ prendre la valeur de la matriceTF par l'appelle de la fonction construire_matrice_tf, 
        ensuite transposer la matrice, pour rendre les lignes de la matrice répresentées par mots et les colonnes
        représentées par documents. Afin de faciliter le calcul """
        matrice_tf=self.construire_matrice_tf(vocab)
        Tmatrice_tf=np.transpose(matrice_tf)
        for i, mot in enumerate(vocab):
           total_occurrencesOfWord_in_corpus = Tmatrice_tf[i].sum()
           # Count documents that contain the word
           count_document_contain_word = np.count_nonzero(Tmatrice_tf[i])
           vocab[mot]["Total_NbrOccurences"] = total_occurrencesOfWord_in_corpus
           vocab[mot]["Nbr_Documents"] = count_document_contain_word
           print(f"Progress: {round((i+1)*100/len(vocab),2)}%") #Cet affichage a pour but de déterminer l'avancement d'execution du code 
        return vocab,Tmatrice_tf
    ############ Q1.4 ##########
    def construire_matrice_tfidf(self,vocab):
        # calcule la matrice Tf et ajouter vocabulaire
        vocabulaireModifie,Tmatrice_tf= self.modification_vocab_calcul(vocab)
        mat_tf=np.transpose(Tmatrice_tf)
        # Calculer la matrice IDF
        nbr_documents_contenant_mot=[]
        for mot in vocabulaireModifie:
            nbr_documents_contenant_mot.append(vocabulaireModifie[mot]["Nbr_Documents"])
        idf = np.log((self.ndoc + 1) / (np.array(nbr_documents_contenant_mot) + 1)) + 1
        # Step 3: Calculer la matrice TF-IDF
        mat_tfidf = np.multiply(mat_tf,idf)
        return mat_tfidf
    
####################################### Test et Validation ########################################
####### Q3.4 #########
# Test=Corpus('TestValidation')
# Test.Add(Document('Test','Betbaut','05-01-2023','www.arxiv.com/AiTest','Test Test Validation validation Q3.4'))
# Test.display_sorted_documents(2,'date')
# Test.save()
# Test.load()
########### TD6: Q1.1 ###########
#passages_trouves = Test.search("deep learning")
#print(passages_trouves)
############## TD6: Q1.2 ##########
#resultats_concorde = Test.concorde("deep learning", 12)
#print(resultats_concorde)
############## TD6: Q2.1/Q2.2/Q2.3/Q2.4 ########
#CleanTexte=Test.nettoyer_texte("Ceci est un Exemple 123 avec hyr?@;;{!des. Ponctuations! et des\npassages à la ligne.")
#print(CleanTexte)
#freq = Test.construire_vocabulaire_et_calculer_occurrences()
#print(freq)

############# TD7 #############"
# vocabulaire__informations = Test.construire_vocab_informations()
# print(vocabulaire__informations)
# matriceTF=Test.construire_matrice_tf(vocabulaire__informations)
# print(matriceTF)
# print("******************************************************************")
# vocabulaire_modifie,TmatrixTF=Test.modification_vocab_calcul(vocabulaire__informations)
# print(vocabulaire_modifie)
# print("**********************************************")
# print(TmatrixTF)
# matriceTFIDF = Test.construire_matrice_tfidf(vocabulaire__informations)
# print(matriceTFIDF)
