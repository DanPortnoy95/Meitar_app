import streamlit as st
import duckdb as ddb
import pandas as pd
import plotly.express as px


# Naming the app
st.set_page_config(page_title="מקהלת מיתר - ניהול נתונים", layout="wide")

# Connecting to our DataBase
@st.cache_resource
def db_connect():
    conn = ddb.connect('C:\\Users\\User\\Documents\\projects\\meitar project\\Data\\meitar_db.db', read_only=True)
    conn.execute("SET search_path = 'meitar_project,main'")
    return conn

# Caching the tables
@st.cache_data
def load_repertoire():
    conn = db_connect()
    # Querying the full table, and joining with category descriptions for clarity
    query = """
    SELECT 
        c.description as category_name
        , r.*
    FROM Repertoire r
    LEFT JOIN Category c ON r.category = c.category;
    """
    return conn.execute(query).df()

@st.cache_data
def load_performance():
    conn = db_connect()
    # querying the whole performance table
    # This should be cleaned and done with joining to the repertoire table, but need to figure a break case of piece performed that was not included in the repertoire.
    query = """
    SELECT 
        *
    FROM Performance p
    ORDER BY p.date DESC, p.performance_order ASC;
    """
    return conn.execute(query).df()

# Side-bar 
st.sidebar.title("🎶 מקהלת מיתר")
page = st.sidebar.radio("ניווט:", ["חיפוש ברפרטואר", "ניתוח הופעות וסטטיסטיקה"])

# Search Page
if page == "חיפוש ברפרטואר":
    st.header("🔎 חיפוש וסינון ברפרטואר")

    df_rep = load_repertoire()

    col1, col2 = st.columns([3,1])
    with col1:
        search_text = st.text_input("טקסט לחיפוש:")
    with col2:
        all_cats = ["הכל"] + df_rep['category_name'].dropna().unique().tolist()
        search_by = ["הכל", "category", "serial", "title", "composer", "arranger", "lyrics", "translator", "language",
                     "voicing", "instruments"]
        selected_cat = st.selectbox("סנן לפי קטגוריה:", all_cats)
        
        # Dynamically get columns to avoid KeyError, excluding the category description
        searchable_columns = [col for col in df_rep.columns if col != 'category_name']
        filter_by = st.selectbox("חפש לפי עמודה:", selected_cat if selected_cat != "הכל" else searchable_columns)
    
    filtered_df = df_rep.copy()
    if search_text:
        # Search by user input
        filtered_df = filtered_df[filtered_df[filter_by].astype(str).str.contains(search_text, case=False, na=False)]
    if selected_cat != "הכל":
        filtered_df = filtered_df[filtered_df['category_name'] == selected_cat]

    if filtered_df.shape[0]==0:
        st.write("לא נמצאו יצירות מתאימות")

    else:
        st.write(f"נמצאו {len(filtered_df)} יצירות:")
        st.dataframe(filtered_df, use_container_width=True)

elif page == "ניתוח הופעות וסטטיסטיקה":
    st.header("📊 ניתוח הופעות וסטטיסטיקה")

    df_perf = load_performance()
    # Ensure date is datetime for filtering
    df_perf['date'] = pd.to_datetime(df_perf['date'], errors='coerce', dayfirst=True)

    # Time range selection
    st.subheader("פופולריות יצירות")
    time_range = st.radio(
        "בחר טווח זמן:",
        ["הכל", "5 שנים אחרונות", "3 שנים אחרונות"],
        horizontal=True
    )

    # Apply time filter
    current_year = pd.Timestamp.now().year
    if time_range == "5 שנים אחרונות":
        df_perf = df_perf[df_perf['date'].dt.year >= (current_year - 5)]
    elif time_range == "3 שנים אחרונות":
        df_perf = df_perf[df_perf['date'].dt.year >= (current_year - 3)]

    if df_perf.empty:
        st.info("אין נתוני הופעות לטווח הזמן הנבחר.")
    else:
        # Calculate most popular pieces
        top_pieces = df_perf['piece_title'].value_counts().reset_index()
        top_pieces.columns = ['piece_title', 'count']

        # Create Histogram (Bar chart of counts)
        fig = px.bar(top_pieces.head(10), x='count', y='piece_title', orientation='h',
                     title=f"10 היצירות המבוצעות ביותר ({time_range})",
                     labels={'count': 'מספר ביצועים', 'piece_title': 'שם היצירה'},
                     template="plotly_white")
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)