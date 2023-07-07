import openai
import streamlit as st

# Get the OpenAI key from the Streamlit secrets
openai.api_key = os.getenv("openaikey")

# Define the guide, supervisor, and nature element
guide_role = "Guide"
supervisor_role = "Supervisor"
nature_role = None  # This will be determined by the supervisor

# Define the conversation history
conversation_history = []

# Define the function to chat with GPT-3
def chat_with_gpt3(role, user_question, system_message_content):
    system_message = {
        "role": "system",
        "content": system_message_content
    }
    user_message = {
        "role": "user",
        "content": user_question
    }
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[system_message, user_message]
    )
    return response['choices'][0]['message']['content']

# User's conversation with the guide
st.header('Conversation with the Guide')
user_input = st.text_input("Enter your feelings about nature and the element you want to talk to:")
if user_input:
    guide_response = chat_with_gpt3(guide_role, user_input, f"You are the {guide_role} in an interactive decision tree game. Your role is to help the user navigate the game, understand the rules, and provide support when needed.")
    st.write(guide_response)
    conversation_history.append((user_input, guide_response))

    # Supervisor's analysis
    supervisor_response = chat_with_gpt3(supervisor_role, user_input, f"You are the {supervisor_role} in an interactive decision tree game. Your role is to analyze the user's responses and determine the nature element they want to talk to.")
    nature_role = extract_nature_element(supervisor_response)  # You need to implement this function

    # User's conversation with the nature element
    if nature_role:
        st.header(f'Conversation with {nature_role}')
        user_input = st.text_input(f"Enter your question to {nature_role}:")
        if user_input:
            nature_response = chat_with_gpt3(nature_role, user_input, f"You are {nature_role}, a sentient entity with feelings, desires, and a personality. You're capable of feeling joy when humans take care of the environment, and sadness when they don't. You can communicate with humans and express your feelings.")
            st.write(nature_response)
            conversation_history.append((user_input, nature_response))

            # Supervisor's analysis
            supervisor_response = chat_with_gpt3(supervisor_role, user_input, f"You are the {supervisor_role} in an interactive decision tree game. Your role is to analyze the user's responses and determine if they have hit all the checkpoints.")
            missing_checkpoints = extract_missing_checkpoints(supervisor_response)  # You need to implement this function

            # Guide's suggestions
            if missing_checkpoints:
                guide_response = chat_with_gpt3(guide_role, f"The user is missing the following checkpoints: {missing_checkpoints}", f"You are the {guide_role} in an interactive decision tree game. Your role is to help the user navigate the game, understand the rules, and provide support when needed.")
                st.sidebar.write(guide_response)
