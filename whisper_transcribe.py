import os
import json
from dotenv import load_dotenv
from groq import Groq



def get_text_from_audio(filename):
    load_dotenv()


    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Open the audio file
    with open(filename, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
        file=file, # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="verbose_json",  # Optional
        timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
        language="fr",  # Optional
        temperature=0.0  # Optional
        )
        # To print only the transcription text, you'd use print(transcription.text) (here we're printing the entire transcription object to access timestamps)

        return transcription.text

if __name__ == "__main__":
    filename = os.path.dirname(__file__) + "/Grouv.wav" # Replace with your audio file!
    text = get_text_from_audio(filename)
    print(text)