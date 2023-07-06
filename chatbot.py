import openai

openai.api_key = 'your-api-key'

response = openai.ChatCompletion.create(
  model="gpt-4",  # Assuming GPT-4 is available
  messages=[
        {"role": "system", "content": "You are a knowledgeable entity about climate change."},
        {"role": "user", "content": "What are the main causes of climate change?"},
    ]
)

print(response['choices'][0]['message']['content'])
