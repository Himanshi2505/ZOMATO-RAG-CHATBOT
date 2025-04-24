from rag_chatbot import RestaurantRAG

rag = RestaurantRAG()

# Example usage in Streamlit
import streamlit as st

st.title("Zomato Restaurant Intelligence Assistant")
user_query = st.text_input("Ask a question about restaurants, menus, or dietary options:")

if user_query:
    answer = rag.query(user_query)
    st.write(answer)
