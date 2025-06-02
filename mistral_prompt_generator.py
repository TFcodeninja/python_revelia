import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from whisper_transcribe import get_text_from_audio
from pathlib import Path

load_dotenv()

def generate_prompt(transcribed_text, style="onirique, poétique"):
    """
    Utilise l’API Mistral pour transformer un texte de rêve en prompt artistique.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    model = "mistral-large-latest"
    client = MistralClient(api_key=api_key)

    message = (
        f"Voici un rêve raconté par un humain :\n\n"
        f"{transcribed_text}\n\n"
        f"Transforme ce rêve en une description d’image visuelle détaillée, "
        f"comme un prompt pour une IA d’image (Stable Diffusion ou DALL·E).\n"
        f"Le style doit être : {style}."
    )

    response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=message)]
    )

    return response.choices[0].message.content.strip()



def get_prompt_from_audio(audio_file_path):
    """
    Transcrit un audio avec Groq, puis génère un prompt artistique via Mistral.
    """
    transcription = get_text_from_audio(audio_file_path)
    prompt = generate_prompt(transcription)
    return prompt


if __name__ == "__main__":
    audio_path = Path(__file__).parent / "Grouv.wav"
    prompt = get_prompt_from_audio(audio_path)
    print("\n🎨 Prompt généré :\n", prompt)
