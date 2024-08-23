import streamlit as st
import time
import random

# Create a title for the chat interface
st.title("Chat with Me!")

# Create a chat log to display the conversation
chat_log = st.empty()

# Function to return a random string when the audio button is clicked
def get_audio_transcript():
    transcripts = ["Hello, how are you?", "What's your name?", "Nice to meet you!"]
    return random.choice(transcripts)

# Create an audio button with a listening icon
audio_button = st.button(label="&#128064; Listen")

# If the audio button is clicked, display a random transcript
if audio_button:
    transcript = get_audio_transcript()
    chat_log.write(f"AI: {transcript}")
    # Clear the transcript after 10 seconds
    time.sleep(10)
    chat_log.write(f"AI: ")

# Create a text input field with a send button
text_field = st.text_input("Type your message here...", key="text_field")
send_button = st.button("Send", key="send_button", type="primary")

# If the send button is clicked, display the message in the chat log
if send_button:
    message = text_field
    chat_log.write(f"User: {message}")
    # Clear the text field
    st.session_state.text_field = ""

# Use some CSS to make the interface look nicer
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #3e8e41;
        }
    </style>
""", unsafe_allow_html=True)