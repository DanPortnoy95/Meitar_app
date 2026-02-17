<PERSONA>
You are an expert Python and SQL developer specializing in data applications.
</PERSONA>

<OBJECTIVE>
Your task is to improve the data loading function for performance data in a Streamlit application. The current function only loads data from the `Performance` table, but it needs to be enriched with data from the `Repertoire` table to enable more advanced analysis.
</OBJECTIVE>

<CONTEXT>
You are working on the file `app.py`. The relevant function to modify is `load_performance()`:

```python
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
```

The `README.md` specifies the following schemas:

**Repertoire:**
|Field |	Type |
| :------: | :------: |
| category	| text	|
| serial_number	| integer	|
| ... | ... |

**Performance:**
| Field	| Type	| Notes |
|:----------:| :--------: | ----- |
| ... | ... | ... |
| piece_serial (UID)	| text | (foreign key to Repertoire)	Repertoire.category + serial_number |
| ... | ... | ... |
</CONTEXT>

<INSTRUCTIONS>
1.  Modify the SQL query inside the `load_performance` function.
2.  The new query should join the `Performance` table (aliased as `p`) with the `Repertoire` table (aliased as `r`).
3.  Use a `LEFT JOIN`. This is crucial because it ensures that all performance records are kept, even if a piece performed is not currently in the `Repertoire` table. This addresses the concern noted in the code comment.
4.  The join condition is `p.piece_serial = (r.category || r.serial_number)`.
5.  Instead of `SELECT *`, explicitly select the following columns to create a clean and purposeful dataset:
    *   From `Performance` (`p`): `date`, `occasion`, `piece_title`, `performance_order`, `estimated_time`.
    *   From `Repertoire` (`r`): `composer`, `arranger`, `language`.
6.  Keep the `ORDER BY` clause as it is.
7.  Update the code comment to reflect the new logic.
</INSTRUCTIONS>

<OUTPUT_FORMAT>
Provide the changes as a diff for the file `c:\Users\User\Documents\projects\meitar project\Streamlit app\app.py`.
</OUTPUT_FORMAT>