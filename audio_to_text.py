import requests
import base64

def transcribe_audio(audio_data, source_language):
    # Read the uploaded file and encode it into Base64
    # audio_data = base64.b64encode(uploaded_file.read()).decode("utf-8")

    # Prepare the JSON payload
    payload = {
        "config": {
            "language": {
                "sourceLanguage": source_language  # Accepts source language
            },
            "transcriptionFormat": {
                "value": "transcript"
            },
            "audioFormat": "wav",  # Make sure the uploaded file is in .wav format
            "samplingRate": 16000,
            "postProcessors": None
        },
        "audio": [
            {
                "audioContent": audio_data
            }
        ],
        "controlConfig": {
            "dataTracking": True
        }
    }

    # Send the POST request
    response = requests.post(
        "https://demo-api.models.ai4bharat.org/inference/asr/conformer",
        json=payload
    )

    # Convert response to JSON
    response_data = response.json()

    # Extract the transcription output
    if response.status_code == 200 and 'output' in response_data:
        transcription_output = response_data['output'][0]['source']
        return transcription_output
    else:
        return f"Error: {response.status_code}, {response_data}"

# # Example usage
# transcription = transcribe_audio("test.wav", "ta")
# print(transcription)
