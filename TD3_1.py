# Importation de toutes librairies utilisées
import praw 
import urllib
import xmltodict 
import pandas as pd
from datetime import datetime
import json
########################## Partie1: Chargement des données ########################################
docs=[]
titles_liste=[]
authors_liste=[]
publicationDate_liste=[]
urls_liste=[]
################## Q-1.1 ################
# creation une instance de praw pour appeler l'Api reddit
reddit = praw.Reddit(client_id='KfpBYWFwoxuZX15VsZu1vA', client_secret='TXmLbkY9WpUbD0VgURtegAQSiKAPow', user_agent='ScrapingR')
# Selection de la  thématique (subreddit) AI artificial intelligence
subreddit = reddit.subreddit('artificial')
# Scraping and parsing top <= 300 text in subreddit artificial, then add text to docs list
for post in subreddit.hot(limit=300):
     post.selftext = post.selftext.replace('\n',' ')
     docs.append(post.selftext)
     titles_liste.append(post.title)
     author=post.author.name if post.author else 'Unknown Author'
     authors_liste.append(author)
     datePublication=datetime.utcfromtimestamp(post.created_utc).strftime('%d-%m-%Y')
     publicationDate_liste.append(datePublication)
     postLink="https://www.reddit.com"+post.permalink
     urls_liste.append(postLink)
# Validation du code précedent
print(authors_liste[0],'\n',publicationDate_liste[0],'\n',titles_liste[0],'\n',urls_liste[0])
print(len(authors_liste),'\t',len(publicationDate_liste),'\t',len(titles_liste),'\t',len(urls_liste))
assert len(authors_liste)==len(publicationDate_liste)==len(titles_liste)==len(urls_liste)
docs.append('Seperation between Reddit documents or texts and Arxiv posts') # add this element to the list just for seperation between reddit content and Xriv content
################## Q-1.2  ################
query = "AI"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=300'
url_read = urllib.request.urlopen(url).read()
# url_read est un "byte stream" qui a besoin d'être décodé
scrapedData =  url_read.decode()
ParsedData = xmltodict.parse(scrapedData) #xmltodict permet d'obtenir un objet ~JSON
Articles = ParsedData['feed']['entry']
for d in Articles:
    texte = d['summary']
    texte = texte.replace("\n", " ")
    docs.append(texte)
    title=d['title'].replace("\n"," ")
    titles_liste.append(title)
    datePublication= datetime.strptime(d.get('published', ''),'%Y-%m-%dT%H:%M:%SZ').strftime('%d-%m-%Y')
    publicationDate_liste.append(datePublication)
    authors=d.get('author', '')
    authors = ['Unknown Author' if isinstance(author, str) else author['name'] for author in authors]
    authors='/'.join(authors) # Combine tous les noms des auteurs par une chaine de caractère
    authors_liste.append(authors)
    PaperLink=[entry['@href'] for entry in d.get('link', {})][0]
    urls_liste.append(PaperLink)

# Validation du code précedent
print(authors_liste[-1],'\n',publicationDate_liste[-1],'\n',titles_liste[-1],'\n',urls_liste[-1])
print(len(authors_liste),'\t',len(publicationDate_liste),'\t',len(titles_liste),'\t',len(urls_liste))
assert len(authors_liste)==len(publicationDate_liste)==len(titles_liste)==len(urls_liste)
########################## Partie 2 : sauvegarde des données ########################################

############ Q_2.1 ###########
# Get the index of element that seperate texts of Reddit and Arxiv
indexOfSeperation=0
for j,i in enumerate(docs):
     if i == 'Seperation between Reddit documents or texts and Arxiv posts':
          indexOfSeperation=j
          print(indexOfSeperation)
          break
# Add id and origine of texts 
ids=[]
origine=[]

for indice,document in enumerate(docs):
   if indice<indexOfSeperation:
       ids.append(f'Reddit_{indice}') 
       origine.append('Reddit')
   elif indice==indexOfSeperation:
      pass 
   else:
       ids.append(f'Arxiv_{indice-indexOfSeperation-1}') 
       origine.append('Arxiv')

# suppression l'element de la separation de la liste docs
docs.pop(indexOfSeperation)
# Ensemble de listes pour les méta_données
meta_data = {
    "titles": titles_liste,
    "authors": authors_liste,
    "links": urls_liste,
    "Publiction_dates": publicationDate_liste,
    "documents": docs
}

# Chemin du fichier JSON qui rassemble toutes les listes qui contiennent méta_données des documents extraits de Reddit/ Arxiv
chemin_fichier_json = "metadata_listes.json"
# Écriture de l'ensemble de listes dans le fichier JSON
with open(chemin_fichier_json, 'w') as fichier_json:
    json.dump(meta_data, fichier_json)

# Create dataFrame includes all texts and ids, origines
data={'Id':ids,'Content':docs,'Origine':origine}
Df=pd.DataFrame(data)

############ Q_2.2 ###########
# Exporter à le disque dur les données sous format csv séparé par tabulations au place des virgules at sous le nom Data
Df.to_csv('Data.csv', sep='\t', index=False)




