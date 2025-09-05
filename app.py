import streamlit as st
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
temp_book = pickle.load(open('temp_book.pkl', 'rb'))
sample_books = pt.index.tolist()

# Set config
st.set_page_config(page_title="Book Recommender", layout="wide", page_icon="📚")

# Initialize session state
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = "Home"

# Inject Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f4f7fc;
        }

        .navbar {
            background-color: #ffffff;
            padding: 16px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .navbar-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }

        .navbar-buttons {
            display: flex;
            gap: 10px;
        }

        .book-card {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            padding: 12px;
            margin-bottom: 20px;
            background-color: white;
            transition: transform 0.3s ease;
        }

        .book-card:hover {
            transform: translateY(-5px);
        }

        .book-image-border {
            border: 3px solid transparent;
            border-radius: 12px;
            background-image: linear-gradient(white, white), 
                              linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet);
            background-origin: border-box;
            background-clip: content-box, border-box;
        }

        .stTextInput > div > input {
            background-color: #ffffff;
        }

        h5, p {
            color: #222;
        }
    </style>
""", unsafe_allow_html=True)

# Custom Navbar with Streamlit Buttons
col1, col2, col3 = st.columns([3, 2, 6])
with col1:
    st.markdown("<div class='navbar-title'>📘 Book Recommender</div>", unsafe_allow_html=True)
with col2:
    pass
with col3:
    nav_col1, nav_col2 = st.columns([1, 1])
    with nav_col1:
        if st.button("🏠 Home"):
            st.session_state.nav_page = "Home"
    with nav_col2:
        if st.button("📚 Recommend"):
            st.session_state.nav_page = "Recommendation"

# Home Page
def home_page():
    st.markdown("## 📚 Top 50 Books")
    cols_per_row = 4

    for i in range(0, len(popular_df), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(popular_df):
                book = popular_df.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class='book-card'>
                            <img src="{book['Image-URL-M']}" class='book-image-border' style='width: 100%; height: auto; border-radius: 8px;'/>
                            <h5 style="margin-top: 10px;">{book['Book-Title']}</h5>
                            <p style="margin-bottom: 4px;">👤 {book['Book-Author']}</p>
                            <p style="margin-bottom: 0;">⭐ {book['avg_ratings']:.2f} | 🗳️ {book['num_ratings']}</p>
                        </div>
                    """, unsafe_allow_html=True)

# Recommendation Page
def recommendation_page():
    st.markdown("## 🔍 Book Recommendation")
    st.markdown("#### Search for a book to get personalized recommendations:")

    col1, col2 = st.columns([2, 3])

    with col1:
        select_book_name = st.text_input(
            'Enter Book Name', 
            value='Harry Potter and the Chamber of Secrets (Book 2)'
        )
    
    with col2:
        selected_suggestion = st.selectbox("Or pick from suggestions:", sample_books, index=0)

    final_input = select_book_name.strip() if select_book_name.strip() else selected_suggestion

    if st.button('🚀 Get Recommendation'):
        if final_input in sample_books:
            index = np.where(pt.index == final_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]

            st.markdown(f"### 📘 Because you liked: **{final_input}**")
            cols_per_row = 4

            for i in range(0, len(similar_items), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(similar_items):
                        ind = similar_items[i + j][0]
                        name = pt.index[ind]

                        book_match = temp_book[temp_book['Book-Title'].str.strip().str.lower() == name.strip().lower()]
                        if not book_match.empty:
                            author = book_match['Book-Author'].values[0]
                            image_link = book_match['Image-URL-M'].values[0]

                            with cols[j]:
                                st.markdown(f"""
                                    <div class='book-card'>
                                        <img src="{image_link}" class='book-image-border' style='width: 100%; height: auto; border-radius: 8px;'/>
                                        <h5 style="margin-top: 10px;">{name}</h5>
                                        <p style="margin-bottom: 4px;">👤 {author}</p>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.warning(f"No image/author found for {name}")
        else:
            st.error("⚠️ Book not found. Please try a different title.")

# Page routing logic
if st.session_state.nav_page == "Home":
    home_page()
elif st.session_state.nav_page == "Recommendation":
    recommendation_page()
