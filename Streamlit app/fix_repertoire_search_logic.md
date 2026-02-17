<PERSONA>
You are an expert Streamlit and Pandas developer with a keen eye for user interface design and robust filtering logic.
</PERSONA>

<OBJECTIVE>
Your task is to refactor the repertoire search page in a Streamlit application. The current implementation has a bug where the column selection for searching breaks when a category is selected. The goal is to create a more intuitive and functional search experience.
</OBJECTIVE>

<CONTEXT>
You are working on the file `app.py`. The relevant section is under the `if page == "חיפוש ברפרטואר":` block:

```python
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
```
</CONTEXT>

<INSTRUCTIONS>
1.  **Restructure the UI**: Change the layout from two columns (`st.columns([3,1])`) to three columns (`st.columns([2, 1, 1])`) for a more balanced appearance.
    *   The first column will contain the text input (`search_text`).
    *   The second column will contain the category filter (`selected_cat`).
    *   The third column will contain a new dropdown for selecting which column(s) to search in.

2.  **Decouple Filters**: The category filter and the text search should be independent. The current logic is flawed. The filtering should be applied sequentially.

3.  **Improve Search Column Selection**:
    *   Remove the old `filter_by` selectbox.
    *   In the new third column, create a `selectbox` labeled "חפש בעמודה:".
    *   The options for this new selectbox should be a predefined list of user-friendly, searchable text columns (e.g., `["הכל", "title", "composer", "arranger", "lyrics", "translator", "language", "voicing", "instruments"]`).

4.  **Refactor Filtering Logic**:
    *   First, apply the category filter if a category other than "הכל" is selected.
    *   Second, apply the text search filter *only if* `search_text` is not empty.
    *   If the user chose a specific column to search in (e.g., "composer"), filter the DataFrame on that single column.
    *   If the user chose "הכל" for the search column, the search should be performed across *all* the major text columns. You can achieve this by creating a boolean mask that checks if the `search_text` appears in any of the specified columns for each row.

5.  Ensure the logic correctly handles `NaN` values by converting columns to string type (`.astype(str)`) before performing the `.str.contains()` operation.
</INSTRUCTIONS>

<OUTPUT_FORMAT>
Provide the changes as a diff for the file `c:\Users\User\Documents\projects\meitar project\Streamlit app\app.py`.
</OUTPUT_FORMAT>