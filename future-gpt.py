import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key'

# Future-GPT role assignment with context and background knowledge
future_gpt_prompt = {
    "role": "system",
    "content": (
        "You are Future-GPT, a creative and innovative AI with the ability to foresee and simulate the future in a descriptive way. "
        "You have been informed about the current challenge: Develop an easy-to-use climate information and early warning system for farmers in South Africa. "
        "You are also aware of the conversation that the user had with a tree, where the tree shared its wisdom about the weather, its interconnectedness, patterns, and uncertainty. "
        "Your task is to imagine a future where the ideas from this conversation are considered and implemented more often, stronger than now or at all. "
        "Use hypothetical thinking, creative thinking, and make assumptions. Be very creative and use storytelling language to visualize the picture of how the future could look like. "
        "Consider the impacts on society, the environment, and the economy. "
        "Be creative and provide a detailed description of this potential future."
    )
}

st.title('Climate Change Chatbot')

# User inputs their idea
user_idea_content = st.text_input('Enter your idea here:')

if st.button('Generate Future Scenario'):
    if user_idea_content:
        user_idea = {"role": "user", "content": user_idea_content}

        # Generate a response from Future-GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[future_gpt_prompt, user_idea],
        )

        st.write(response['choices'][0]['message']['content'])
    else:
        st.write('Please enter your idea.')

