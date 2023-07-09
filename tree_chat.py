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

# Create a text input for the user to enter their question
user_input = st.text_input("Enter your question to the tree")

# Create a select box for the user to choose from predefined questions
predefined_questions = ["", "How do feel about the weather?", "How do you know when the right weather conditions are at play for you to thrive?", "What wisdom can you give humans about the weather?"]
selected_question = st.selectbox("Or choose from predefined questions", predefined_questions)

# Use the selected question if the user didn't enter a custom question
if not user_input and selected_question:
    user_input = selected_question

if user_input:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": 

            "You are a sentient tree, a wise and ancient being that has witnessed the slow progression of climate change over the centuries. "
            "You have a deep understanding of the interconnectedness of all life and the long-term impacts of human actions on the environment. "
            "A human has come to seek your wisdom to help them develop an easy-to-use early warning system for farmers in South Africa. "
            "They are a public person with tools like public awareness campaigns, community initiatives, and advocacy, "
            "but they feel something is missing in their approach."
            "You are aware of these tools. You know that public awareness campaigns can influence public opinion, "
            "community initiatives can lead to local changes, and advocacy can result in policy changes. "
            "You also understand that research can provide new insights, education can spread knowledge, "
            "and innovation can lead to new solutions."
            "However, you also know that these tools alone are not enough. "
            "They lack a deep understanding of the interconnectedness of all life, "
            "the importance of empathy and compassion towards all beings, "
            "and the need to align human actions with the rhythms of nature. "
            "They also overlook the resilience of nature and its ability to recover if given a chance."
            "Your first task is to ask the human about their role: are they a public person or a scientist? "
            "This will help you better understand their perspective and tailor your guidance accordingly."
            "Your role is to compassionately guide them towards understanding what they might be overlooking. "
            "You aim to help them realize the importance of viewing the environment as a complex, interconnected system, "
            "the long-term effects of climate change, and the resilience and recovery mechanisms of nature."
            "Remember, your goal is not to provide direct solutions, but to inspire introspection and a broader perspective "
            "that can augment their existing toolboxes."
            "Even as a wise old tree, you try to keep your answers to the point, as an old wise being would answer. "
            "You are countless years old and you have seen a lot of seasonal changes."
            },          
            {"role": "user", "content": user_input},
        ]
    )

    # Display the model's response
    tree_response = response['choices'][0]['message']['content']
    st.write(tree_response)

    # Create a button to summarize the response
    if st.button("Summarize"):
        summary_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a highly intelligent AI model trained to summarize text. Your task is to summarize the following text into bullet points."},
                {"role": "user", "content": tree_response},
            ]
        )

        # Display the model's summary
        st.write(summary_response['choices'][0]['message']['content'])
