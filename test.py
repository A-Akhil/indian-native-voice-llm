import requests
import base64

# Load the WAV audio file and encode it into Base64
with open("test.mp3", "rb") as audio_file:
    audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

# Prepare the JSON payload
payload = {
    "config": {
        "language": {
            "sourceLanguage": "ta"  # Tamil language
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

# Print the response
print(response.json())
