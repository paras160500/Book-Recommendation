import streamlit as st
import pickle 
import numpy as np 

popular_df = pickle.load(open('popular.pkl' , 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl' , 'rb'))
pt = pickle.load(open('pt.pkl' , 'rb'))
temp_book = pickle.load(open('temp_book.pkl' , 'rb'))
sample_books = pt.index.tolist()

# Set page config
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# Home Page
def home_page():
    st.title("Top 50 Books")
    cols_per_row = 4 

    for i in range(0,len(popular_df),cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(popular_df):
                book = popular_df.iloc[i+j]
                with cols[j]:
                    st.image(book['Image-URL-M'], use_container_width=True)
                    st.markdown(book['Book-Title'])
                    st.markdown(book['Book-Author'])
                    st.markdown("Votes: " + str(book['num_ratings']))
                    st.markdown("Ratings: " + str(book['avg_ratings']))
                    

# About Page
def about_page():
    st.title("Book Recommendation Page")
    select_book_name = ""
    select_book_name = st.text_input('Enter Book Name Here' ,value='Harry Potter and the Chamber of Secrets (Book 2)' )
    
    if st.button('Get Recommendation'):
        if select_book_name != "":
            
            if select_book_name in sample_books:
                index = np.where(pt.index == select_book_name)[0][0]
                similar_items = sorted(list(enumerate(similarity_score[index])),key= lambda x : x[1] , reverse=True)[1:9]

                cols_per_row = 4
                for i in range(0, len(similar_items), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        if i + j < len(similar_items):
                            ind = similar_items[i + j][0]
                            name = pt.index[ind]
                            author = temp_book[temp_book['Book-Title'] == name]['Book-Author'].values[0]
                            image_link = temp_book[temp_book['Book-Title'] == name]['Image-URL-M'].values[0]

                            with cols[j]:
                                st.image(image_link, use_column_width=True)
                                st.markdown(f"**{name}**")
                                st.markdown(f"*by {author}*")
                    
            else:
                st.title("Book not Found")
    

# Page routing
if page == "Home":
    home_page()
elif page == "About":
    about_page()