import requests
import base64

def transcribe_audio(file_path, source_language):
    # Load the WAV audio file and encode it into Base64
    with open(file_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

    # Prepare the JSON payload
    payload = {
        "config": {
            "language": {
                "sourceLanguage": source_language  # Accepts source language
            },
            "transcriptionFormat": {
                "value": "transcript"
            },
            "audioFormat": "wav",
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

# Example usage
transcription = transcribe_audio("test.wav", "ta")
print(transcription)
