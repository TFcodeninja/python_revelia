import os
import replicate
from dotenv import load_dotenv

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")

os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

def generate_image(prompt):
    """
    Génère une image à partir d’un prompt avec Stable Diffusion via Replicate.
    """
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion",
            input={"prompt": prompt}
        )
        return output[0]  # URL de l'image générée
    except Exception as e:
        print(f"Erreur génération image : {e}")
        return None