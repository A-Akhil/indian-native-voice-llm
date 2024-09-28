import ollama as client

# Function to get response from Ollama API with system prompt
def get_ollama_response(text):
    system_prompt = "You are a bot and speaks in one lines. Keep your responses short and to the point."
    stream = client.chat(
        model="tinyllama",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        stream=True
    )
    
    response = ''
    for chunk in stream:
        response += chunk['message']['content']
    return response
