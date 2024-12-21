# coding=utf8
from gtts import gTTS
import gradio as gr
import os
import speech_recognition as sr
from googletrans import Translator
from moviepy import *


def video_to_translate(file_obj, initial_language, final_language):
    # Insert Local Video File Path
    videoclip = VideoFileClip(file_obj.name)
    # Extract audio from the video
    videoclip.audio.write_audiofile("test.wav", codec="pcm_s16le")

    # Initialize the recognizer
    r = sr.Recognizer()

    # Map input language to recognition language codes
    lang_codes_in = {
        "English": "en-US",
        "Italian": "it-IT",
        "Spanish": "es-MX",
        "Russian": "ru-RU",
        "German": "de-DE",
        "Japanese": "ja-JP",
        "Portuguese": "pt-BR",
        "Tamil": "ta-IN",
        "Hindi": "hi-IN",
        "Kannada": "kn-IN",
        "Telugu": "te-IN",
    }
    lang_in = lang_codes_in[initial_language]

    # Open the file
    with sr.AudioFile("test.wav") as source:
        # Listen for the data (load audio to memory)
        audio_data = r.record(source)
        # Recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language=lang_in)

    # Map output language to Google Translate language codes
    lang_codes_out = {
        "English": "en",
        "Italian": "it",
        "Spanish": "es",
        "Russian": "ru",
        "German": "de",
        "Japanese": "ja",
        "Portuguese": "pt",
        "Tamil": "ta",
        "Hindi": "hi",
        "Kannada": "kn",
        "Telugu": "te",
    }
    lang_out = lang_codes_out[final_language]

    # Initialize the Google API translator
    translator = Translator()
    translation = translator.translate(text, dest=lang_out)
    trans = translation.text

    # Generate audio from the translated text
    myobj = gTTS(text=trans, lang=lang_out, slow=False)
    myobj.save("audio.wav")

    # Load the audio file
    audioclip = AudioFileClip("audio.wav")
    # Add the audio to the video clip
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    new_video = f"video_translated_{lang_out}.mp4"
    videoclip.write_videofile(new_video)
    return new_video


# Input options
initial_language = gr.inputs.Dropdown(
    [
        "English",
        "Italian",
        "Japanese",
        "Russian",
        "Spanish",
        "German",
        "Portuguese",
        "Tamil",
        "Hindi",
        "Kannada",
        "Telugu",
    ]
)
final_language = gr.inputs.Dropdown(
    [
        "English",
        "Italian",
        "Japanese",
        "Russian",
        "Spanish",
        "German",
        "Portuguese",
        "Tamil",
        "Hindi",
        "Kannada",
        "Telugu",
    ]
)

# Custom CSS for the updated theme
css = """
body {
    background-color: #e6ffe6; /* Light green background */
}
.gradio-container {
    background-color: #e6ffe6; /* Light green container background */
    border: none;
}
.gr-input, .gr-button {
    background-color: #ffffff; /* White input fields and buttons */
    color: #004d00; /* Dark green text */
    border: 1px solid #66ff66; /* Bright green border */
}
.gr-button:hover {
    background-color: #66ff66; /* Bright green hover effect */
    color: #003300;
}
h1 {
    color: #004d00; /* Dark green heading */
    font-family: Arial, sans-serif;
    font-weight: bold;
    text-align: center;
}
"""

# Interface creation
gr.Interface(
    fn=video_to_translate,
    inputs=["file", initial_language, final_language],
    outputs="video",
    verbose=True,
    title="Quadra Translate",
    description="Translate video files between various languages. Upload your video and process it easily!",
    article="""<div style="text-align: center; color: #004d00;">
                <p>Upload an MP4 file and hit submit to translate the video. Click Play/Pause to view the video. 
                The video is saved in MP4 format.</p>
                <p>For more information, visit <a href="https://ruslanmv.com/" style="color: #004d00;">ruslanmv.com</a>.</p>
               </div>""",
    css=css,
).launch()
