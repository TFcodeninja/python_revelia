import os
import sys
import streamlit as st
import tempfile

# 👉 Ajouter le dossier parent dans le path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Maintenant les imports fonctionnent
from backend.whisper_transcribe import transcribe_audio
from backend.mistral_prompt_generator import generate_prompt
from backend.stable_diffusion_generator import generate_image
from backend.storage import init_db, store_dream

# Initialiser la base
init_db()

st.set_page_config(page_title="Be Real - Générateur de Rêves", layout="centered")
st.title("💭 Be Real — Transforme ton rêve en image")

st.markdown("Décris ton rêve par la voix, et regarde-le prendre vie ✨")

# 1. Upload fichier audio
audio_file = st.file_uploader("🎙️ Enregistre ton rêve (format .mp3 ou .wav)", type=["mp3", "wav"])

if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tmp_audio.write(audio_file.read())
        audio_path = tmp_audio.name

    st.audio(audio_path)

    if st.button("🚀 Générer l'image de ton rêve"):
        with st.spinner("📝 Transcription en cours..."):
            transcription = transcribe_audio(audio_path)

        if transcription:
            st.success("✅ Transcription réussie")
            st.write(f"**Ton rêve :** {transcription}")

            with st.spinner("✨ Génération du prompt..."):
                prompt = generate_prompt(transcription)

            if prompt:
                st.success("✅ Prompt généré")
                st.write(f"**Prompt artistique :** {prompt}")

                with st.spinner("🎨 Génération de l’image..."):
                    image_url = generate_image(prompt)

                if image_url:
                    st.image(image_url, caption="🖼️ Rêve illustré")
                    store_dream(prompt, transcription, image_url)
                    st.success("💾 Rêve sauvegardé avec succès")
                else:
                    st.error("❌ Erreur lors de la génération de l’image")
            else:
                st.error("❌ Échec de la création du prompt")
        else:
            st.error("❌ Erreur dans la transcription audio")
