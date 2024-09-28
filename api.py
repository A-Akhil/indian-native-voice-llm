import requests
import ollama as client

# Language mapping dictionary
language_map = {
    "Bangla": "bn",
    "English": "en",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Malayalam": "ml",
    "marathi (Bengali script)": "mr",
    "Odia": "or",
    "Punjabi (Gurmukhi script)": "pa",
    "Sanskrit": "sa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

# Function to get the language code from the provided language name or code
def get_language_code(language):
    # Check if the input is already a code
    if language in language_map.values():
        return language
    # Check if the input is a language name
    return language_map.get(language.strip(), None)

# Function to translate text using the AI4Bharat API
def translate_text(text, source_lang, target_lang):
    url = "https://demo-api.models.ai4bharat.org/inference/translation/v2"
    payload = {
        "controlConfig": {
            "dataTracking": True
        },
        "input": [
            {
                "source": text
            }
        ],
        "config": {
            "serviceId": "",
            "language": {
                "sourceLanguage": source_lang,
                "targetLanguage": target_lang,
                "targetScriptCode": None,
                "sourceScriptCode": None
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("output", [{}])[0].get("target", "No output found")
    else:
        print(f"Translation failed. Status code: {response.status_code}")
        return None

# Function to get response from Ollama API with system prompt
def get_ollama_response(text):
    system_prompt = "You are a bot and speaks in one lines. Keep your responses short and to the point."
    stream = client.chat(
        model="tinyllama",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text+"reply like a user and negotiate the amount for 1kg potato to 30rs dont go below it"}
        ],
        stream=True
    )
    
    response = ''
    for chunk in stream:
        response += chunk['message']['content']
    return response

def llama_api(text_to_translate,source_language):
    # Input from the user
    # text_to_translate = input("Enter the text to translate: ")

    # Convert language names to codes
    source_language_code = get_language_code(source_language)

    if not source_language_code:
        return "Invalid source language code or name selection."

    # Translate text to English
    english_text = translate_text(text_to_translate, source_language_code, "en")
    if not english_text:
        return "Failed to translate text to English."

    # Get response from Ollama
    ollama_response = get_ollama_response(english_text)

    # Translate response back to the original language
    final_translation = translate_text(ollama_response, "en", source_language_code)
    if final_translation:
        return final_translation
    else:
        return "Failed to translate the response."
# 
# if __name__ == "__main__":
#     result = llama_api()