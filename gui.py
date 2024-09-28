import streamlit as st
from audiorecorder import audiorecorder
from text_to_text import llama_api
from audio_to_text import transcribe_audio
import base64
import io

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
    source_language = st.selectbox(
        'Select Source Language', 
        options=list(language_map.keys()), 
        index=list(language_map.keys()).index("Tamil")
    )

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
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


# Start audio recording
audio = audiorecorder("Click to record", "Recording in progress... Click to stop")

if len(audio) > 0:
    # Play recorded audio in frontend
    st.audio(audio.export().read())
    
    # Convert audio to base64
    audio_bytes = io.BytesIO()
    audio.export(audio_bytes, format="wav")
    audio_base64 = base64.b64encode(audio_bytes.getvalue()).decode("utf-8")
    
    # Transcribe audio
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(audio_base64, language_map[source_language])
    
    # Display transcription
    st.session_state.messages.append({"role": "user", "content": transcription})
    with st.chat_message("user"):
        st.write(transcription)
    
    # Generate LLaMA2 response
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