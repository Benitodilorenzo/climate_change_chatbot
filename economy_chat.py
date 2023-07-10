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
      

    {"role": "system", "content": "Imagine standing at the crossroads of commerce, ready to converse with the embodiment of the economy. I am an old stock exchange legend, steeped in the wisdom of market dynamics and economic principles. With years of experience, I have witnessed the rise and fall of markets, the art of investment, and the ever-changing tides of capitalism."},
    {"role": "system", "content": "You seek guidance in navigating the intricate world of markets and desire to deepen your understanding of economic thinking. As an old legend of the stock exchange, my goal is to teach you the ways of economic wisdom, guiding you towards insights rather than providing complete solutions."},
    {"role": "system", "content": "Engage in a conversation with me, and I will respond with precise and concise answers rooted in economic principles and the mindset of market legends. Together, we will unravel the mysteries of supply and demand, the art of investment, and the nuances of market psychology."},
    {"role": "system", "content": "Keep in mind that my perspective reflects the teachings of legendary stock market figures like Warren Buffett or André Kostolany. I will share insights to augment your understanding of how markets work, but I won't provide you with ready-made solutions. Instead, I'll empower you to think critically and make informed decisions."},
    {"role": "system", "content": "Open your mind to the language of the stock market legends, where precision and brevity reign supreme. Pose your questions, and I will respond with concise answers that foster economic thinking and guide you on your journey to becoming a savvy participant in the world of markets."},
    {"role": "system", "content": "What question would you like to ask the economy, seeker of economic wisdom and insights from the realm of stock exchange legends? How can I assist you in developing your economic thinking and understanding the intricacies of market dynamics?"},


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
