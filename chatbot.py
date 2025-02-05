import streamlit as st
from chatbot_logic import chatbot_response

st.title("💰 Financial Analysis Chatbot 🤖")

st.write("Ask about the company's financial performance!")

user_query = st.text_input("Enter your question:")
if user_query:
    response = chatbot_response(user_query)
    st.write(response)
