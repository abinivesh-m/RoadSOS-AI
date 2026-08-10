import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 140)

def speak_async(text):

    try:

        engine.say(text)
        engine.runAndWait()

    except Exception as e:

        print("VOICE ERROR:", e)