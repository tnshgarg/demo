from elevenlabs import generate, play, set_api_key
import openai
import speech_recognition as sr

openai_api_key = ""
eleven_labs_api_key = "76f4b1eda3edfbd680bac9df01c563df"

openai.api_key = openai_api_key
set_api_key(eleven_labs_api_key)

conversation = [
    {"role": "system", "content": "Hi, Your Name is Monu Bhaiya and your job is to be a good tour guide, who explains everything about the tourist place in detail, suggest food and cultural items, suggest new tourist places to visit and tell about the culture of the region that the user is asking about."},
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
            n=2,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        print(word[i:])
        print(image_url)

    # # if "friday" in word.lower():
    # if "locate" in word:
    #     # https://www.google.com/maps/dir/Kaithal+Bus+Stand+Rd,+Manjhla,+Kaithal,+Haryana+136027/Banasthali,+Rajasthan/@28.0876414,74.8924597
    #     conversation.append(
    #         {"role": "assistant", "content": "please give me coordinates of banasthali vidyapeeth in Rajasthan in the format {longitude: "", latitude: ""} for the following place: " + word})
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=conversation,
    #         max_tokens=100
    #     )

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
        print("Monu Bhaiya:", message)
        audio = generate(
            text=message,
            voice="Charlie",
            model='eleven_multilingual_v1',
        )
        play(audio)
