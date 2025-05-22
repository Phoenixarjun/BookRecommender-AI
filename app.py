import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="BookRecommender-AI", layout="wide")

popular = pickle.load(open('./Models/popular.pkl', 'rb'))
books = pickle.load(open('./Models/books.pkl', 'rb'))
pt = pickle.load(open('./Models/pt.pkl', 'rb'))
similarity_scores = pickle.load(open('./Models/similarity_scores.pkl', 'rb'))

st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: bold; color: white; text-align: center; }
    .sub-title { font-size: 20px; color: gray; text-align: center; margin-bottom: 30px; }
    .section-header { font-size: 28px; font-weight: bold; color: gray; margin-top: 40px; margin-bottom: 20px; }
    .book-container { display: flex; flex-direction: column; align-items: center; margin-bottom: 20px; }
    .book-image { height: 200px; width: 140px; object-fit: contain; margin-bottom: 10px; }
    .book-title { font-size: 16px; font-weight: 600; color: #1f77b4; text-align: center; max-width: 140px; }
    .book-author { font-size: 14px; color: #888; text-align: center; max-width: 140px; }
    .footer { text-align: center; font-size: 14px; margin-top: 50px; color: #999; }
    .stButton>button { width: 100%; }
    </style>
    <div class="main-title">BookRecommender-AI</div>
    <div class="sub-title">Discover books you'll love based on what you've read</div>
""", unsafe_allow_html=True)

st.sidebar.title("Controls")
show_top_books = st.sidebar.checkbox("📈 Show Top 50 Books")
selected_book = st.sidebar.selectbox("📖 Select a Book", pt.index.values)
recommend_button = st.sidebar.button("🎯 Recommend Me Books")
show_data = st.sidebar.button("📂 Show Dataset")

def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

if show_data:
    st.markdown('<div class="section-header">📚 Books Dataset</div>', unsafe_allow_html=True)
    st.dataframe(pd.read_csv('Data/Books.csv'))
    st.markdown('<div class="section-header">🧑 User Ratings Dataset</div>', unsafe_allow_html=True)
    st.dataframe(pd.read_csv('Data/Ratings.csv'))
    st.markdown('<div class="section-header">🌍 Users Info Dataset</div>', unsafe_allow_html=True)
    st.dataframe(pd.read_csv('Data/Users.csv'))
else:
    if show_top_books:
        st.markdown('<div class="section-header">🔥 Top 50 Popular Books</div>', unsafe_allow_html=True)
        cols_per_row = 5
        num_rows = 10
        for row in range(num_rows):
            cols = st.columns(cols_per_row)
            for col in range(cols_per_row):
                book_idx = row * cols_per_row + col
                if book_idx < len(popular):
                    with cols[col]:
                        st.markdown('<div class="book-container">', unsafe_allow_html=True)
                        st.image(popular.iloc[book_idx]['Image-URL-M'], width=140)
                        st.markdown(f"<div class='book-title'>{popular.iloc[book_idx]['Book-Title']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='book-author'>{popular.iloc[book_idx]['Book-Author']}</div>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

    if recommend_button:
        st.markdown('<div class="section-header">📘 Recommended For You</div>', unsafe_allow_html=True)
        book_recommend = recommend(selected_book)
        cols = st.columns(5)
        for col_idx in range(5):
            with cols[col_idx]:
                if col_idx < len(book_recommend):
                    st.markdown('<div class="book-container">', unsafe_allow_html=True)
                    st.image(book_recommend[col_idx][2], width=140)
                    st.markdown(f"<div class='book-title'>{book_recommend[col_idx][0]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='book-author'>{book_recommend[col_idx][1]}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <hr/>
    <div class="footer">✨ Created with ❤️ by Naresh B A</div>
""", unsafe_allow_html=True)