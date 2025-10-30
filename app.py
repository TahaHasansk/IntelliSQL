import streamlit as st
import os
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))




def get_response(question):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt = """
You are an expert in converting English questions to SQL queries.
The database is called STUDENTS and has columns: NAME, CLASS, MARKS, COMPANY.

Examples:
Q: How many entries of records are present?
A: SELECT COUNT(*) FROM STUDENTS;

Q: Tell me all the students studying in MCom class?
A: SELECT * FROM STUDENTS WHERE CLASS='MCom';
"""

    input_text = f"{prompt}\n\nQ: {question}"
    response = model.generate_content(input_text)
    raw_output = response.text.strip()

    # ✅ Remove markdown code blocks and backticks
    raw_output = raw_output.replace("```sql", "").replace("```", "").replace("`", "").strip()

    # ✅ Remove the 'A:' if present
    if raw_output.lower().startswith("a:"):
        raw_output = raw_output[2:].strip()

    # ✅ Extract just the first valid SQL statement (usually ends at semicolon)
    if ";" in raw_output:
        sql_statement = raw_output.split(";")[0].strip() + ";"
    else:
        sql_statement = raw_output.strip()

    return sql_statement







def read_query(sql, db="data.db"):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        rows = [[f"Error: {e}"]]
    conn.commit()
    conn.close()
    return rows


def page_home():
    st.markdown("""
    <style>
    body {
        background-color: #2E2E2E;
    }
    .main-title {
        text-align: center;
        color: #4CAF50; /* Green color for headings */
        font-size: 2.5em;
    }
    .sub-title {
        text-align: center;
        color: #4CAF50; /* Green color for headings */
        font-size: 1.5em;
    }
    .offerings {
        padding: 20px;
        color: white; /* White color for body text */
    }
    .offerings h2 {
        color: #4CAF50; /* Green color for headings */
    }
    .offerings ul {
        list-style-type: none;
        padding: 0;
    }
    .offerings li {
        margin: 10px 0;
        font-size: 18px;
    }
    .custom-sidebar {
        background-color: #2E2E2E;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Welcome to IntelliSQL!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Revolutionizing Database Querying with Advanced LLM Capabilities</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
       st.markdown(
    "<img src='https://cdn-icons-png.flaticon.com/512/4248/4248443.png' width='250' style='display: block; margin-left: auto; margin-right: auto;'>",
    unsafe_allow_html=True
)

    with col2:
        st.markdown("""
        <div class='offerings'>
        <h2>Wide Range of Offerings</h2>
        <ul>
            <li>💡 Intelligent Query Assistance</li>
            <li>📊 Data Exploration and Insights</li>
            <li>⚡ Efficient Data Retrieval</li>
            <li>📈 Performance Optimization</li>
            <li>📝 Syntax Suggestions</li>
            <li>📈 Trend Analysis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
def page_about():
    st.markdown("""
    <style>
    .content {
        color: white; /* White color for body text */
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: #4CAF50;'>About IntelliSQL</h1>", unsafe_allow_html=True)
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.markdown("""
    <h2>IntelliSQL is an innovative project aimed at revolutionizing database querying using advanced Language Model capabilities.</h2>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    "<img src='https://cdn-icons-png.flaticon.com/512/190/190411.png' width='200' style='display: block; margin-left: auto; margin-right: auto;'>",
    unsafe_allow_html=True
)

def page_intelligent_query_assistance():
    st.markdown("""
    <style>
    .tool-input {
        margin-bottom: 20px;
        color: white; /* White color for body text */
    }
    .response {
        margin-top: 20px;
        color: white; /* White color for body text */
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color: #4CAF50;'>Intelligent Query Assistance</h1>", unsafe_allow_html=True)
    st.write("""
    IntelliSQL enhances the querying process by providing **intelligent assistance** to users. Whether they are novice or experienced S
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='tool-input'>", unsafe_allow_html=True)
        que = st.text_input("Enter Your Query:", key="sql_query")
        submit = st.button("Get Answer", key="submit_button", help="Click to retrieve the SQL data")
        st.markdown("</div>", unsafe_allow_html=True)

        if submit or que:
            try:
                sql_query = get_response(que)
                st.write(f"***Generated SQL Query:*** `{sql_query}`")
                results = read_query(sql_query, "data.db")
                st.markdown("<div class='response'>", unsafe_allow_html=True)
                st.subheader("The Response is:")
                st.table(results)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.subheader("Error:")
                st.error(f"An error occurred: {e}")

    with col2:
        st.markdown(
    "<img src='https://cdn-icons-png.flaticon.com/512/983/983601.png' width='220' style='display: block; margin-left: auto; margin-right: auto;'>",
    unsafe_allow_html=True
)

def main():
    st.set_page_config(
        page_title="IntelliSQL",
        page_icon="💡",
        layout="wide"
    )
    st.sidebar.title("Navigation")
    st.sidebar.markdown("<style>.sidebar .sidebar-content {background-color: #2E2E2E; color: white;}</style>", unsafe_allow_html=True)
    pages = {
        "Home": page_home,
        "About": page_about,
        "Intelligent Query Assistance": page_intelligent_query_assistance,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
