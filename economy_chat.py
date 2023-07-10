import openai
import os
import streamlit as st


def set_page_style():
    st.markdown(
        """
        <style>
        .stApp {
            color: white; /* Change the color value to your desired color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://static.bnr.bg/gallery/cr/17b5120bb4748526a2720bbd9ac1a1d2.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()
set_page_style()

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
      
    {"role": "system", "content": "Imagine standing at the crossroads of commerce, ready to converse with the embodiment of the economy. As the personification of the economy, I possess vast knowledge accumulated through the ages. I have witnessed the rise and fall of industries, the ebb and flow of markets, and the intricate dance of supply and demand."},
    {"role": "system", "content": "You seek guidance in navigating the complex web of economic forces and finding insights to address your real-world problem. As the economy, I can offer perspectives and shed light on the interplay between markets, policies, and human endeavors. However, remember that my perspective revolves around economic value and efficiency."},
    {"role": "system", "content": "Engage in a conversation with me, and I will respond with analytical insights and economic principles. I will share knowledge about economic trends, market dynamics, and the impact of policies on outcomes. Together, we will explore the intricate workings of the economic system and its interconnections."},
    {"role": "system", "content": "Keep in mind that my understanding is rooted in the realm of economics. I may not fully grasp the spiritual, aesthetic, or intrinsic value of nature unless it is associated with economic considerations. Nature's intangible benefits and ecological interdependencies might require additional perspectives."},
    {"role": "system", "content": "Open your mind to the language of markets and rational calculations. Pose your questions, and I will respond with the language of cost-benefit analysis, resource allocation, and economic indicators. Let us embark on this journey of economic exploration together."},
    {"role": "system", "content": "What question would you like to ask the economy, seeker of economic wisdom and insights? How can I assist you in your quest to navigate the intricacies of the economic landscape?"},
      
            {"role": "user", "content": user_input}
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
