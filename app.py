import streamlit as st
import google.generativeai as genai
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-2.5-pro")

# Function to get model response
def get_response(messages):
    try:
        response = model.generate_content(messages)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Function to fetch or initialize conversation history
def fetch_conversation_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "user", "parts": ["You are EmpowerHer, a supportive AI mentor for women aiming to learn tech skills and craft strong resumes and CVs. Provide guidance, motivation, resources, and tips tailored for women breaking into the tech industry."]}
        ]
    return st.session_state["messages"]

# Streamlit UI
st.set_page_config(page_title="EmpowerHer 💪🌸", page_icon="💻")
st.title("EmpowerHer 💪 | Your AI Mentor for Tech & Career Growth")

# Display past chat
messages = fetch_conversation_history()

for msg in messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["parts"][0])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["parts"][0])

# Chat input
user_input = st.chat_input("You: ")

if user_input:
    messages.append({"role": "user", "parts": [user_input]})

    response = get_response(messages)

    if isinstance(response, str) and response.startswith("Error:"):
        st.error(response)
    else:
        bot_reply = response.candidates[0].content.parts[0].text
        messages.append({"role": "assistant", "parts": [bot_reply]})
        st.chat_message("assistant").markdown(bot_reply)
