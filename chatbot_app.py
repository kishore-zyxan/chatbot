import streamlit as st
from db_config import get_db_engine
from sql_generator import generate_sql_from_question
from utils import run_query

st.set_page_config(page_title="SambaNova SQL Chatbot")

st.title("💬 SambaNova SQL Chatbot")
st.write("Ask your database a question using natural language:")

question = st.text_input("Enter your question:")

if st.button("Submit"):
    if question:
        with st.spinner("Processing..."):
            sql_query = generate_sql_from_question(question)
            st.code(sql_query, language="sql")

            engine = get_db_engine()
            columns, data = run_query(engine, sql_query)

            if columns and data:
                st.success("Query Result:")
                st.dataframe([dict(zip(columns, row)) for row in data])
            else:
                st.error(data)  # error message
    else:
        st.warning("Please enter a question to proceed.")
