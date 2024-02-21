from dotenv import load_dotenv
from elevenlabs import generate, play, set_api_key
import os
from gtts import gTTS
import openai
import speech_recognition as sr
from flask import Flask

app = Flask(__name__)

load_dotenv()


def chatgpt():

    openai_api_key = "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"
    eleven_labs_api_key = "76f4b1eda3edfbd680bac9df01c563df"

    openai.api_key = openai_api_key
    set_api_key(eleven_labs_api_key)

    conversation = [
        {"role": "system", "content": "Your name is JARVIS and your purpose is to be Tanish's AI assistant with a flair for sass. Keep it stylish and on-point! Summarize your answers in less than 75 words"},
    ]

    while True:
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Please say something:")
            audio = r.listen(source)
            print("Recognizing...")

        try:
            print("You said:", r.recognize_google(audio))
            word = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand the audio!")
        except sr.RequestError:
            print("Could not request results; check your network connection!")

        if "draw" in word:
            i = word.find("draw")
            i += 5
            response = openai.Image.create(
                prompt=word[i:],
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            print(word[i:])
            print(image_url)

        # if "friday" in word.lower():

        elif "stop" in word:
            break

        else:
            conversation.append({"role": "assistant", "content": word})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                max_tokens=100
            )

            message = response["choices"][0]["message"]["content"]

            conversation.append({"role": "assistant", "content": message})
            print("Pepper said (with sass):", message)
            # tts = gTTS(text=message, lang='en-GB')
            # tts.save("response.mp3")
            # os.system("mpg321 response.mp3 >/dev/null 2>&1")
            # os.system("sox response.mp3 -d tempo 1.25")
            audio = generate(
                text=message,
                voice="Charlie",
                model='eleven_multilingual_v1',
            )
            play(audio)


@app.route("/")
def hello():
    return chatgpt()


if __name__ == "__main__":
    app.run()
