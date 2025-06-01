import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRAL_KEY")

def generate_prompt(transcribed_text, dream_style="onirique"):
    """
    Utilise l'API Mistral pour transformer un texte de rêve en prompt artistique.
    """
    client = Mistral(api_key=api_key)

    message = f"""
    Tu es un assistant créatif. Reformule le rêve suivant en un prompt clair et imagé
    pour générer une illustration via une IA d'image. Ajoute un style '{dream_style}'.

    Rêve : {transcribed_text}
    """

    try:
        response = client.chat(
            model="mistral-medium",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erreur Mistral : {e}")
        return None