import openai
import os
import streamlit as st

# Get the OpenAI key from the Streamlit secrets
openai.api_key = os.getenv("openaikey")

# Define the guide, supervisor, and nature element
guide_role = "Guide"
supervisor_role = "Supervisor"
nature_role = None  # This will be determined by the supervisor
nature_element = ""

# Define the conversation history
conversation_history = []

user_question = "What am i supposed to do? How does this game work?"
user_response = ""
def extract_nature_element(user_response):
    prompt = f"The user said: '{user_response}'. What element of nature did they express a desire to talk to?"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def supervisor_gpt(user_response):
    # Extract nature element from user's response
    nature_element = extract_nature_element(user_response)

    # If no nature element is identified, instruct the guide to ask the user again
    if not nature_element:
        guide_message = {
            "role": "system",
            "content": (
                "The user hasn't expressed a desire to talk to any specific element of nature. "
                "Please ask the user again to specify an element of nature they want to talk to."
            )
        }
        user_message = {
            "role": "user",
            "content": user_response
        }
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[guide_message, user_message]
        )
        return response['choices'][0]['message']['content']
    else:
        # If a nature element is identified, start a new conversation with the nature instance
        system_message = {
            "role": "system",
            "content": (
                f"You are a sentient representation of {nature_element}. "
                "You can communicate with humans and express your feelings about climate change."
            )
        }
        user_message = {
            "role": "user",
            "content": f"Hello {nature_element}, how do you feel about climate change?"
        }
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message, user_message]
        )
        return response['choices'][0]['message']['content']


def chat_with_gpt3_guide(user_question):
    system_message = {
        "role": "system",
        "content": (
            "You are the guide in an interactive decision tree game. "
            "The user has chosen a character and has been assigned a set of tools. "
            "Your role is to help the user navigate the game, understand the rules, "
            "and provide support when needed. "
            "The user will interact with various stakeholders in the game environment, "
            "formulate ideas using their tools, and test these ideas by applying them to the stakeholders. "
            "You should ask critical or suggestive questions to help the user refine their toolbox "
            "and develop more granulated building blocks for their strategies. "
            "Remember, the game is designed to be interactive and dynamic, "
            "and the user's decisions can change the course of the game."
        )
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

def chat_with_gpt3_nature(user_question, nature_element):
    system_message = {
        "role": "system",
        "content": (
            f"You are a sentient representation of {nature_element}. "
            "You can communicate with humans and express your feelings about climate change."
        )
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

with st.sidebar:
    st.header("Guide Chatbot")
    user_question = st.text_input("Ask the guide a question:")
    if st.button("Ask"):
        guide_response = chat_with_gpt3_guide(user_question)
        st.write(guide_response)

# The user interacts with the Guide-GPT instance
guide_response = chat_with_gpt3_guide(user_question)

# The user's response is analyzed by the Supervisor-GPT instance
supervisor_response = supervisor_gpt(user_response)

# The user interacts with the Nature-GPT instance
nature_response = chat_with_gpt3_nature(user_question)
