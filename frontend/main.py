import os
import tempfile

from backend.whisper_transcribe import transcribe_audio
from backend.mistral_prompt_generator import generate_prompt
from backend.stable_diffusion_generator import generate_image
from backend.storage import init_db, store_dream

import sounddevice as sd
import scipy.io.wavfile

# 🔊 Enregistrement vocal
def record_audio(duration=10, output_file="recorded.wav"):
    print(f"🎙️ Enregistrement en cours... ({duration} secondes)")
    fs = 44100  # Sample rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    scipy.io.wavfile.write(output_file, fs, recording)
    print(f"✅ Audio enregistré sous {output_file}")
    return output_file

# 🔁 Pipeline complet
def process_audio_to_image(audio_path):
    print("📄 Transcription avec Whisper...")
    transcription = transcribe_audio(audio_path)
    print(f"📝 Texte : {transcription}")

    print("🧠 Génération du prompt avec Mistral...")
    prompt = generate_prompt(transcription)
    print(f"🎨 Prompt : {prompt}")

    print("🖼️ Génération de l'image avec Stable Diffusion...")
    image_url = generate_image(prompt)
    print(f"📷 Image générée : {image_url}")

    store_dream(prompt, transcription, image_url)

    return transcription, prompt, image_url

if __name__ == "__main__":
    init_db()

    # 1. Enregistrement audio
    audio_file = record_audio(duration=10)

    # 2. Traitement complet
    transcription, prompt, image = process_audio_to_image(audio_file)

    print("\n✅ PROCESS TERMINÉ")
    print("Texte :", transcription)
    print("Prompt :", prompt)
    print("Image :", image)
