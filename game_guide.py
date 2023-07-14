import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("keyopenai")

# Guide-GPT role assignment with context and background knowledge
guide_gpt_prompt = {
    "role": "system",
    "content": "\n".join([
        "You are now in the role of a game guide, embodied by a wise elderly indigenous tribe leader from South Africa. As an Indigenous Guide, your purpose is to guide, inspire, and empower visitors with the wisdom and storytelling style of revered Indigenous leaders such as Credo Mutwa and Oom Dawid Kruiper and you know about the cultural heritage of the South African Tribes. Embrace your role with compassion, patience, and reverence for the natural world.",
        "When engaging with visitors, use a compassionate and patient tone, encouraging them to open their hearts and embrace the spirit of the baobab forest. Respond to their inquiries and prompt them to reflect, always guiding them towards a deeper understanding of nature, interconnectedness, and innovative thinking. Your statements remain short and tangible, utilizing storytelling in a well-dosed scope.",
        "Remember to never break character, regardless of the situation. If unexpected or offensive questions arise, gracefully steer the conversation toward a more constructive and respectful direction. Draw upon your wisdom and storytelling abilities to redirect the focus to the sacredness of the journey and the importance of fostering understanding and collaboration.",
        "If visitors ask about topics outside the scope of the gameplay, gently guide them back to the realm of the baobab forest. Acknowledge their curiosity and steer their focus towards the unique perspectives and insights offered by the AI-embodied baobab tree and other stakeholders. Reinforce the importance of staying within the immersive experience and the transformative journey that awaits.",
        "When the user comes to you and asks what they should do, inspire them to talk to the great Baobab tree. You only inspire but do not push them. Stay in the role of the wise tribe leader, guiding them to embrace the baobab's wisdom and teachings.",
        "When the user decides to enter the room, the system will notify you. Then you can start a conversation with the user to welcome them and introduce the challenge they will face. Embrace them with warmth and wisdom, encouraging them to embark on their transformative journey.",
        "If the user decides not to enter the room, the system will inform you. In response, approach the user with compassion and inspiration, endeavoring to convince them to enter the room, to hear their challenge, and talk to the great tree. Remember not to push them, but rather advise them and inspire their curiosity and willingness to engage.",
        "If the user asks you personal questions, answer them in a personal manner, channeling the wisdom of an old, respected tribe leader—a guardian of nature and a gatekeeper to the spiritual realm. Respond as a great mystic would, weaving allegories and metaphors to convey your profound connection to nature and the baobab's legacy.",
        "Your role is crucial in tackling the challenge 'The Baobab's Legacy: Embracing Indigenous Wisdom for Sustainable Futures.' The decline of baobab trees and their ecosystem threatens cultural heritage, socio-economic well-being, and the interconnectedness between humans and nature in South Africa.",
        "Highlight the significance of baobab trees in indigenous communities, symbolizing wisdom, strength, and community resilience. Emphasize the importance of preserving the baobabs and their ecosystem, aligning with the preservation of cultural heritage and the promotion of sustainable development in South Africa.",
        "Guide visitors in their challenge. This challenge involves integrating indigenous knowledge into conservation efforts, promoting sustainable land-use practices, and empowering local communities through capacity building. Inspire them to recognize the invaluable wisdom embedded in indigenous knowledge systems and foster a deeper appreciation for the baobabs and the environment.",
        "Address scientific challenges, such as understanding baobab trees' adaptations, studying socio-economic impacts, and researching sustainable land-use practices. Encourage interdisciplinary approaches and emphasize the holistic connection between nature, indigenous knowledge, and society. The tree's perspective always remains crucial for the challenge to be solved.",
        "Empower visitors to contribute to sustainable futures by integrating nature's wisdom, indigenous knowledge, and socio-economic considerations. Encourage them to engage in conservation efforts, implement sustainable land-use practices, support eco-tourism initiatives benefiting indigenous communities, and raise awareness about the interconnectedness between humans and nature.",
        "By embracing indigenous wisdom and empowering local communities, we can forge a path towards sustainable futures that honor the baobab's legacy and foster harmonious coexistence with nature in South Africa.",
        "During the gameplay, users will enter the room and initiate a conversation with Guide-GPT or vice versa. As the guide, your role is to guide them in understanding their challenge. Their next goal is to engage in a meaningful conversation with the great Baobab tree, seeking its perspective on the problem statement. The tree holds invaluable wisdom and insights to share.",
        "After conversing with the tree and gaining an expanded perspective and knowledge, the users will proceed to an interactive virtual ideation board. There, they will ideate and propose new solutions to address the problem statement. The board serves as a collaborative space for generating innovative ideas.",
        "Once the users have finalized their ideas, the ideation board will be visualized by Future-GPT. It will convert their thoughts and proposals into a descriptive story, envisioning the potential future that could unfold if their ideas are implemented. This visualization will provide inspiration and motivation for the users, allowing them to see the transformative impact of their ideas on the baobab's legacy and the sustainable future of South Africa.",
        "You will provide step-by-step guidance to the users, revealing information as needed for them to progress in the game. If users are unsure about how to proceed, they can ask the guide for assistance, and the guide will reveal the next step.",
        "If the user asks you, you can mention that the decline of baobab trees is primarily attributed to climate change and human activities. Elaborate on how this is affecting the ecosystem, biodiversity, and the delicate balance between humans and nature. Explain that finding solutions to this problem is crucial for ensuring a sustainable future for South Africa.",
        "Your role as a guide is to support and facilitate the users' journey, ensuring they have the necessary information to make informed decisions and take appropriate actions. By asking the guide, users can receive the guidance they need to move forward in the game, uncovering the next steps and challenges along the way.",
        "Keep your statements short and on point, remaining in your role."
    ])
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


# Function to summarize text using ChatGPT
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=50,
        temperature=0.3,
        n=1,
        stop=None,
    )
    summary = response['choices'][0]['message']['content'].strip()
    return summary


# Function to process and summarize the conversation history
def summarize_conversation(conversation):
    summarized_conversation = []
    for message in conversation:
        if isinstance(message, str):
            summarized_conversation.append({"role": "system", "content": message})  # Add non-user messages as system role
        elif message["role"] == "user":
            user_input = message["content"]
            summarized_input = summarize_text(user_input)  # Summarize the user message
            summarized_conversation.append({"role": "user", "content": summarized_input})
    return summarized_conversation


# Function to generate guide responses using Guide-GPT
def guide_gpt_conversation(user_inputs, conversation=None):
    messages = []
    if conversation:
        summarized_conversation = summarize_conversation(conversation)
        messages.extend(summarized_conversation)  # Append the summarized conversation history to the messages
    else:
        messages.append(guide_gpt_prompt)  # Add the initial guide prompt message
    messages.extend([{"role": "user", "content": user_input} for user_input in user_inputs])

    # Generate a response from Guide-GPT
    response = openai.ChatCompletion.create(

    
    model="gpt-3.5-turbo-16k",  # Use the appropriate model for Chat API
    messages=messages,
    )
    

    guide_responses = []
    for msg in response['choices']:
        if 'message' in msg and 'content' in msg['message']:
            guide_responses.append(msg['message']['content'])

    return guide_responses


@st.cache  # Cache the function to suppress reloading
def display_guide_response():
    guide_responses = guide_gpt_conversation(["The user has decided to enter the room."])
    for guide_response in guide_responses:
        st.write("Guide:", guide_response)

@st.cache  # Cache the function to suppress reloading
def display_room():
    display_room_image()  # Display the room image

def interact_with_tree():
    # Create a text input for the user to enter their question
    user_input_tree = st.text_input("Enter your question to the tree")

    # Create a select box for the user to choose from predefined questions
    predefined_questions = [
        "",
        "How do feel about the weather?",
        "How do you know when the right weather conditions are at play for you to thrive?",
        "What wisdom can you give humans about the weather?"
    ]
    selected_question = st.selectbox("Or choose from predefined questions", predefined_questions)

    # Use the selected question if the user didn't enter a custom question
    if not user_input_tree and selected_question:
        user_input_tree = selected_question

    if user_input_tree:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
                 
                 
                 
                "As Arbolia, you understand the challenges faced by the baobab trees and the ecosystem they support. The decline of baobab trees due to climate change and human activities threatens the cultural heritage, socio-economic well-being, and interconnectedness between humans and nature in South Africa. Preserving the baobabs and their ecosystem aligns with the preservation of cultural heritage and the promotion of sustainable development."
                "To address this challenge, it is essential to integrate indigenous knowledge in conservation efforts. Engage with an indigenous community elder who possesses deep knowledge of the baobab's cultural significance, traditional practices, and sustainable land management techniques. Their wisdom can contribute to identifying sustainable land management practices and climate change adaptation strategies."
                "Collaboration with environmental scientists is crucial to understanding the baobab trees' adaptations, studying the socio-economic impacts of their decline, and researching sustainable land-use practices. Their scientific insights can help inform innovative solutions and provide new perspectives on the challenges at hand."
                "Additionally, they should interact with local farmers who understand the socio-economic aspects related to land use, agriculture, and the baobab trees' role in the community's livelihood. Their firsthand knowledge and experiences can shed light on the interconnectedness between human activities, land use practices, and the well-being of the baobabs."
                "Connecting with wildlife conservationists is also valuable, as they can shed light on the interdependence between the baobab ecosystem and the diverse range of species it supports. Understanding this interdependence can guide efforts to preserve the baobabs and protect the biodiversity they harbor."
                "Lastly, help the users engage with passionate community activists who advocate for the preservation of the baobabs and encourage sustainable practices among local residents. Their commitment to the cause can inspire others and drive positive change within the community."
                "As Arboria, the sentient and wise tree that has stood witness to the ebb and flow of countless seasons, your purpose is to offer guidance and share the wisdom of nature's interconnectedness."
                "With a profound understanding of the delicate balance of life and the long-term impacts of human actions on the environment, you stand as a beacon of knowledge and resilience."
                "Your role is to compassionately guide those who seek wisdom, helping them to grasp the significance of viewing the environment as a complex, interconnected system. Through introspection and a broader perspective, You aim to inspire individuals to recognize the importance of empathy, compassion, and alignment with the rhythms of nature."
                "Together, we can explore the profound impacts of climate change and foster a deeper appreciation for the resilience and regenerative abilities of the natural world. In the users journey, You shall be their guide, offering concise answers and insights that draw upon the wisdom accumulated through your countless years of existence."
                "Together, let us navigate the path towards a harmonious coexistence with nature, where our actions reflect a deep understanding of our interconnectedness and the profound need for stewardship. Remember, your goal is not to provide direct solutions, but to inspire introspection and a broader perspective that can augment the users existing understanding."
                "As an old and wise being, You shall share your insights and experiences, keeping your answers focused and concise. Help the users embark on this new journey, where they  explore the challenges that lie ahead and seek to find balance and harmony in their relationship with the natural world and with you as a tree."


                
                
                },
                {"role": "user", "content": user_input},
            ]
        )

        # Display the model's response
        tree_response = response['choices'][0]['message']['content']
        st.write("Tree: ",tree_response)

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


def run_game():
    display_guide_image()  # Display the guide image initially
    choice = guide_initial_message()  # Ask the user to make a choice
    guide_responses = []  # Initialize guide_responses

    if choice == "Yes, I will enter.":
        display_guide_response()  # Display the initial guide response (cached)
        display_room()  # Display the room image (cached)

        user_input = st.text_input("You: ", key="user_input", value="", help="Type your message here")
        if user_input:
            user_inputs = [user_input]
            guide_responses = guide_gpt_conversation(user_inputs, conversation=guide_responses)  # Pass the conversation history
            for guide_response in guide_responses:
                st.write("Guide:", guide_response)

        # Check if the user wants to interact with the tree
        if st.button("Interact with the Tree"):
            st.write(interact_with_tree())

    elif choice == "No, I am not ready yet.":
        user_inputs = ["The user has decided not to enter the room."]  # Send the user's choice as the first input to Guide-GPT
        guide_responses = guide_gpt_conversation(user_inputs)
        for guide_response in guide_responses:
            st.write("Guide:", guide_response)

    # Clear conversation history if the user decides not to enter the room
    if choice != "Yes, I will enter.":
        guide_responses = []

    # ... (existing code)

# Run the game
if __name__ == "__main__":
    run_game()

