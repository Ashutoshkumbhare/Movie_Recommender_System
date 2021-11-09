import pickle
import pandas as pd
import requests
import streamlit as st
file = open('my_data.pkl','rb')
movie_dict = pickle.load(file)
similarity = pickle.load(open('similarities.pkl','rb'))
movies = pd.DataFrame(movie_dict)
# print(movies)

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Which movie do you like?',(movies['title']))
st.write('You selected:', selected_movie_name)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies_id))
    return recommended_movies,recommended_movies_poster

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=120e06d98a5bd680e8f70f42d57c4e18'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


if st.button('Recommende'):
    names, poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
