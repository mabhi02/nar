import os
import time
import base64
import simpleaudio as sa
import errno
import openai
from elevenlabs import generate, voices, play, set_api_key

OPENAI_API_KEY = "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"
ELEVENLABS_API_KEY = "9b74ed5063c874b6b22a1dbb12803140"
ELEVENLABS_VOICE_ID = "tuFYG9DxDz318m9BLte9"

# Set API keys for both OpenAI and Eleven Labs
openai.api_key = OPENAI_API_KEY
set_api_key(ELEVENLABS_API_KEY)

def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)

def play_audio(text):
    # Generate audio with the specified voice ID
    audio = generate(text, voice=ELEVENLABS_VOICE_ID)

    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    with open(file_path, "wb") as f:
        f.write(audio)

    play(audio)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]

def analyze_image(base64_image, script):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
    )

    response_text = response.choices[0].message.content
    return response_text

def main():
    script = []

    while True:
        # path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        # analyze posture
        print("👀 David is watching...")
        analysis = analyze_image(base64_image, script=script)

        print("🎙️ David says:")
        print(analysis)

        play_audio(analysis)

        script = script + [{"role": "assistant", "content": analysis}]

        # wait for 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    main()
