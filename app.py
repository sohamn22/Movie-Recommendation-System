import streamlit as st
import pickle
import pandas as pd
import requests



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommendation System')


# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bd2473a7c79aa5bf4e2629d140f80ef6&language=en-US').format(movie_id)
#     data = response.json
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=bd2473a7c79aa5bf4e2629d140f80ef6&language=en-US'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    full_path = f'https://image.tmdb.org/t/p/w500{poster_path}'
    return full_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances= similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


    
option = st.selectbox(
    "Select A Movie",
    movies['title'].values)


if st.button("Recommend Similar Movies"):
    names,posters = recommend(option)
    col1, col2, col3,col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

    
    

