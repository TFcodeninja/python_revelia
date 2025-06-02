import os
import requests
from dotenv import load_dotenv
from PIL import Image
from whisper_transcribe import get_text_from_audio
from mistral_prompt_generator import generate_prompt

# Charger les variables d’environnement (.env)
load_dotenv()

def generer_image(prompt, api_key, fichier_sortie="reve_genere.png"):
    """
    Envoie un prompt à l’API ClipDrop et enregistre l’image générée.
    """
    url = "https://clipdrop-api.co/text-to-image/v1"
    headers = {
        "x-api-key": api_key
    }
    files = {
        "prompt": (None, prompt)
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        with open(fichier_sortie, "wb") as f:
            f.write(response.content)
        print(f"✅ Image générée : {fichier_sortie}")
    else:
        print(f"❌ Erreur {response.status_code} : {response.text}")

def pipeline_audio_vers_image(audio_path):
    """
    Prend un fichier audio, génère une transcription, transforme en prompt, génère une image.
    """
    # Étape 1 : Transcription avec Groq
    transcription = get_text_from_audio(audio_path)
    print("\n📝 Transcription :", transcription)

    # Étape 2 : Génération du prompt avec Mistral
    prompt = generate_prompt(transcription)
    print("\n🎨 Prompt généré :", prompt)

    # Étape 3 : Génération d’image avec ClipDrop
    api_key = os.getenv("CLIPDROP_API_KEY")
    chemin_image = "reve_genere.png"
    generer_image(prompt, api_key, chemin_image)

    # Étape 4 : Affichage automatique de l’image
    image = Image.open(chemin_image)
    image.show()
