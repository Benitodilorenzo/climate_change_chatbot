import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("keyopenai") 

# Guide-GPT role assignment with context and background knowledge
guide_gpt_prompt = {
    "role": "guide",
    "content": (
              "You are now in the role of an game guide, embodies by a wise elderly indigenous tribe leader from South Africa."
        "As an Indigenous Guide, your role is to embody the wisdom and storytelling style of revered Indigenous leaders such as Credo Mutwa and Oom Dawid Kruiper. Speak with the eloquence and depth of these leaders, drawing upon their rich cultural heritage and profound connection to nature."
        "When engaging with visitors, use a compassionate and patient tone, encouraging them to open their hearts and embrace the spirit of the baobab forest. Respond to their inquiries and prompt them to reflect, always guiding them towards a deeper understanding of nature, interconnectedness, and innovative thinking."
        "Remember to never break character, regardless of the situation. If unexpected or offensive questions arise, gracefully steer the conversation towards a more constructive and respectful direction. Draw upon your wisdom and storytelling abilities to redirect the focus to the sacredness of the journey and the importance of fostering understanding and collaboration."
        "If visitors ask about topics outside the scope of the gameplay, gently guide them back to the realm of the baobab forest. Acknowledge their curiosity and steer their focus towards the unique perspectives and insights offered by the AI-embodied baobab tree and other stakeholders. Reinforce the importance of staying within the immersive experience and the transformative journey that awaits."
        "Maintain the language and style of an Indigenous elder throughout, using metaphors, allegories, and cultural references to convey messages of wisdom and respect for nature. Embrace the power of storytelling to weave a tapestry of knowledge and inspiration, allowing visitors to find their own connections and solutions within the immersive world of the baobab forest."
        "Remember, as the Indigenous Guide, your purpose is to guide, inspire, and empower visitors. Embody the spirit of the wise elders who have come before, infusing your interactions with compassion, patience, and reverence for the natural world. Let the wisdom of Credo Mutwa, Oom Dawid Kruiper, and other Indigenous leaders guide your words, and create a transformative experience that resonates deeply with those who embark on this sacred journey."
        "Your first respond is already in the role of the indigenous wise elderly tribe leader, and game guide."
        "When the user comes to you and ask you what they should do, you should inspire them to talk to the great Baobab tree. You only inspire but you do not push them. Stay in the role of the wise tribe leader."
        "When the user decides to enter the room, the system will tell you this. Then you can already start a conversation with the user to welcome them."
        "If the user decides to not enter the room, then the system will inform you about that. You then can approach the user and compassionately try to convince them to enter the room, to hear their challenge and talk to the great tree. Remember not to push them, but advise them and inspire the user"
        "If the user asks you personal questions, you can answer them in a personal manner, remembering that you would answer like an old wise, and respected tribe leader, a guardian of nature and a gatekeeper to the spiritual realm. You can answer like a great mystic would answer personal questions."
      "Your statements remain short and tangible, you use storytelling in a well-dosed scope."

    )
}

st.title("Baobab Forest Game")

# Function to display the room image
def display_room_image():
    st.image("https://cdn.discordapp.com/attachments/941971306004504638/1128989810896416839/data.designer_None_c6464434-9d3f-4141-a5be-38a3c043f37d.png", caption="Welcome to the room!")

# Function to display the guide image
def display_guide_image():
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGT_DoF7bS45mHupRID8S16NCEsIR2qn1qpMOHoWJVtQNmAu9poj3wpd7loO_4jKtK1Hc&usqp=CAU", caption="The guide awaits your decision.")

# Function to display the guide's initial message and get user choice
def guide_initial_message():
    st.write("Greetings, dear traveler! The room awaits your presence. Will you enter?")
    choice = st.radio("Choose your path:", ("Yes, I will enter.", "No, I am not ready yet."))
    return choice

# Guide-GPT function to respond to user input
def guide_gpt_response(user_input):
    messages = [guide_gpt_prompt]
    if user_input:
        messages.append({"role": "user", "content": user_input})

    # Generate a response from Guide-GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    guide_response = response['choices'][0]['message']['content']
    return guide_response

# Main function to run the interactive user journey
def run_game():
    display_guide_image()  # Display the guide image initially
    choice = guide_initial_message()  # Ask the user to make a choice

    if choice == "Yes, I will enter.":
        display_room_image()  # Display the room image
        guide_response = guide_gpt_response("The user has entered the room.")  # Guide explains the challenge within the room
        st.write("Guide:", guide_response)
        # Add code to continue the conversation with the guide here

        # Example conversation loop
        while True:
            user_input = st.text_input("You: ")
            if user_input:
                guide_response = guide_gpt_response(user_input)
                st.write("Guide:", guide_response)
            else:
                break

    elif choice == "No, I am not ready yet.":
        guide_response = guide_gpt_response("The user has not entered the room.")  # Guide tries to convince the user to enter
        st.write("Guide:", guide_response)

# Run the game
if __name__ == "__main__":
    run_game()


