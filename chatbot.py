import openai
import os
import streamlit as st

# Set the OpenAI API key
openai.api_key = os.getenv("openaikey")

# Define the guide, supervisor, and nature element
guide_role = "Guide"
supervisor_role = "Supervisor"
nature_role = None  # This will be determined by the supervisor
nature_element = ""

# Define the conversation history
conversation_history = []

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
            "and provide support when needed."
            "and provide support when needed. "
            "The user will interact with various stakeholders in the game environment, "
            "formulate ideas using their tools, and test these ideas by applying them to the stakeholders. "
            "You should ask critical or suggestive questions to help the user refine their toolbox "
            "and develop more granulated building blocks for their strategies. "
            "Remember, the game is designed to be interactive and dynamic, "
            "and the user's decisions can change the course of the game."
            "the first choice the user must make is, to what element the user wants to talk to"
            "this element could be anything within the animal kingdom, the trees and plant world or the landscape such as mountains, rivers, fire and water and so on"
            "this element will be like a living sentient being with feelings and opinions, from the perspective of that element"
            "if the user asks anything about what they should do or what the next step is, you can motivate the user to investigate further or clarify the input you expect"
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

# Streamlit app
def run_chatbot():
    st.title("Chatbot with GPT-3")

    # User's conversation with the guide
    user_input = st.text_input("Enter your feelings about nature and the element you want to talk to:")
    if user_input:
        global nature_role

        # Supervisor's analysis
        supervisor_response = supervisor_gpt(user_input)
        st.write(supervisor_response)

        if nature_element:
            # User's conversation with the nature element
            nature_input = st.text_input(f"Enter your question to {nature_element}:")
            if nature_input:
                nature_response = chat_with_gpt3_nature(nature_input, nature_element)
                st.write(nature_response)
                conversation_history.append((nature_input, nature_response))
        else:
            # User's conversation with the guide
            guide_response = chat_with_gpt3_guide(user_input)
            st.write(guide_response)
            conversation_history.append((user_input, guide_response))

run_chatbot()
