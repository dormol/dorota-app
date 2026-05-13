from gtts import gTTS
import os

text = "Hello. Your voice AI application is starting clean."

tts = gTTS(text)
tts.save("output.mp3")

os.system("start output.mp3")

