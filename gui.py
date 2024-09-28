import streamlit as st
from text_to_text import llama_api
from audio_to_text import transcribe_audio

# Language mapping
language_map = {
    "Bangla": "bn",
    "English": "en",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi (Bengali script)": "mr",
    "Odia": "or",
    "Punjabi (Gurmukhi script)": "pa",
    "Sanskrit": "sa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

# Streamlit app configuration
st.set_page_config(page_title="🦙💬 Chatbot")

# Sidebar for language selection
with st.sidebar:
    # Dropdown to select the source language
    source_language = st.selectbox(
        'Select Source Language', 
        options=list(language_map.keys()), 
        index=list(language_map.keys()).index("Tamil")
    )

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    language_code = language_map[source_language]
    response = llama_api(prompt_input, language_code)
    return response

# Upload audio file
audio_file = st.file_uploader("Upload Audio File", type=["wav"])

if audio_file:
    # Transcribe the audio file
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(audio_file, language_map[source_language])
    
    # Display the transcription
    st.session_state.messages.append({"role": "user", "content": transcription})
    with st.chat_message("user"):
        st.write(transcription)

    # Generate LLaMA2 response using the transcription
    if transcription:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(transcription)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)

        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
