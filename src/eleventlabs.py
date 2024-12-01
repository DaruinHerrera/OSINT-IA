import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/J3JSkWXJwqClE1dIxQM9"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "sk_c91c7e2ebb5d6c2e9a9ae6e48dba51d7c0d7349dfec55a63"
}

data = {
  "text": "El sol comenzaba a descender, tiñendo el cielo con tonos anaranjados y rosados. En el pequeño pueblo de San Miguel, la vida parecía detenerse al caer la tarde.",
#   "model_id": "eleven_multilingual_v2",
#   "language_code": "spanish",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
#print(response.json())


with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
