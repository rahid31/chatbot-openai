import streamlit as st
import openai
import os
from dotenv import load_dotenv
import shelve
from datetime import datetime

load_dotenv()

# Load the OpenAI API key
client = openai.OpenAI(api_key=os.getenv("API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Session State
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Time Greetings
current_hour = datetime.now().hour
if 5 <= current_hour < 12:
    message = "Good morning!"
elif 12 <= current_hour < 18:
    message = "Good afternoon!"
else:
    message = "Good evening!"


# Streamlit UI
st.title("OpenAI Chatbot") 

if prompt := st.chat_input(f"{message} How can I help you?"):
    # Add user message to chat history
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream the response
        response = client.chat.completions.create(
            model=st.session_state.openai_model,
            messages=st.session_state.messages,
            stream=True,
        )

        # Display the response
        for chunk in response:
            if chunk.choices:
                full_response += chunk.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})