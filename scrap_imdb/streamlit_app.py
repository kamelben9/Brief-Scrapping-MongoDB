import streamlit as st
from pymongo import MongoClient
import pandas as pd


#Connexion à la base de données
client = MongoClient('mongodb://localhost:27017/')

imdb_db = client.mongo_imdb

#récupération des données de la base
imdb = imdb_db.Films.find({})

#Transformation en Dataframe
df = pd.DataFrame(imdb)

print(df)

# Titre
def search_by_title(title):
    return df[df['title'].str.contains(title.title(), na=False)]

# Acteurs
def search_by_acteurs(acteurs):
    return df[df['acteurs'].str.contains(acteurs.title(), na=False)]

# Genre
def search_by_genre(genre):
    return df[df['genre'].str.contains(genre.title(), na=False)]

# Durée
def search_by_duree(durée):
    return df[df['durée'] <= durée]

# Score
def search_by_score(score):
    return df[df['score'] >= score]



st.title("Movie Finder")
st.text("Trouvez le meilleur film pour vous !")
st.image(image = "scrap_imdb/Film.jpg")

with st.sidebar :
    st.sidebar.title("Choix des paramètres")

    # Formuler le nom du film
    film_name = st.sidebar.text_input("Entrez le nom du film:", "")

    # Formuler le genre
    film_genre = st.sidebar.selectbox("Choisissez le genre:", df.genre.unique())

    # Formuler la note minimale
    min_rating = st.sidebar.slider("Note minimale:", 0, 10, 5)

    # Formuler la durée
    max_duration = st.sidebar.slider("Durée maximale:", 0, 300, 120)

    # Formuler les acteurs
    acteurs = st.sidebar.multiselect("Choisir les acteurs:", df.acteurs.unique())