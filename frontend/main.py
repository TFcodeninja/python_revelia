from backend.whisper_transcribe import transcribe_audio
from backend.mistral_prompt_generator import generate_prompt
from backend.stable_diffusion_generator import generate_image
from backend.storage import init_db, store_dream

def main():
    print("Initialisation de la base de données...")
    init_db()

    # Étape 1 : chemin vers ton audio local
    audio_path = "assets/reve_test.mp3"  # à adapter selon ton fichier

    print("\n Transcription de l'audio...")
    transcription = transcribe_audio(audio_path)
    if not transcription:
        print(" Échec de la transcription.")
        return
    print(f" Transcription : {transcription}")

    print("\n Génération du prompt avec Mistral...")
    prompt = generate_prompt(transcription)
    if not prompt:
        print(" Échec de la génération du prompt.")
        return
    print(f" Prompt généré : {prompt}")

    print("\n Génération de l’image avec Stable Diffusion...")
    image_url = generate_image(prompt)
    if not image_url:
        print(" Échec de la génération de l'image.")
        return
    print(f" Image générée : {image_url}")

    print("\n Enregistrement dans la base de données...")
    store_dream(prompt, transcription, image_url)
    print(" Sauvegarde terminée.")

if __name__ == "__main__":
    main()