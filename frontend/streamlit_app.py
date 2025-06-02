import streamlit as st
import sounddevice as sd
import scipy.io.wavfile
import tempfile
import os

from backend.whisper_transcribe import transcribe_audio
from backend.mistral_prompt_generator import generate_prompt
from backend.stable_diffusion_generator import generate_image
from backend.storage import init_db, store_dream

init_db()

st.set_page_config(page_title="Be Real - Rêve vocal en image", layout="centered")
st.title("💭 Be Real — Transforme ton rêve en image")

option = st.radio("🎧 Choisis une méthode :", ["🎙️ Enregistrer", "📁 Uploader un fichier audio"])

audio_path = None

if option == "🎙️ Enregistrer":
    duration = st.slider("⏱️ Durée de l'enregistrement (secondes)", 5, 20, 10)

    if st.button("🎤 Démarrer l'enregistrement"):
        fs = 44100
        st.info("⏺️ Enregistrement en cours...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            scipy.io.wavfile.write(tmpfile.name, fs, recording)
            audio_path = tmpfile.name
            st.success("✅ Enregistrement terminé")
            st.audio(audio_path)

elif option == "📁 Uploader un fichier audio":
    uploaded_file = st.file_uploader("Upload ton rêve (.mp3 ou .wav)", type=["mp3", "wav"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio.write(uploaded_file.read())
            audio_path = tmp_audio.name
        st.audio(audio_path)

# TRAITEMENT
if audio_path and st.button("🚀 Générer l'image"):
    with st.spinner("🧠 Transcription en cours..."):
        transcription = transcribe_audio(audio_path)

    if transcription:
        st.success("📝 Transcription :")
        st.write(transcription)

        with st.spinner("✨ Création du prompt..."):
            prompt = generate_prompt(transcription)

        if prompt:
            st.success("🎨 Prompt généré :")
            st.write(prompt)

            with st.spinner("🎨 Génération de l’image..."):
                image_url = generate_image(prompt)

            if image_url:
                st.image(image_url, caption="🖼️ Ton rêve illustré")
                store_dream(prompt, transcription, image_url)
                st.success("💾 Rêve sauvegardé avec succès !")
            else:
                st.error("Erreur génération image.")
        else:
            st.error("Erreur génération prompt.")
    else:
        st.error("Erreur transcription.")
