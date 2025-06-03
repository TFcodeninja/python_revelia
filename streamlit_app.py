import os
import time
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path


from whisper_transcribe import get_text_from_audio
from mistral_prompt_generator import generate_prompt
from clipdrop_generator import generer_image

# --- CONFIG ---
load_dotenv()
st.set_page_config(page_title="Rêvelia", page_icon="🌙", layout="centered")

# --- CSS ---
def local_css():
    st.markdown("""
        <style>
        body {
            background-color: #0b0c2a;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            font-size: 3em;
            text-align: center;
            margin-bottom: 0;
            color: #f0f0f0;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #aaaaaa;
        }
        .stButton>button {
            background-color: #272a5a;
            color: white;
            border-radius: 10px;
        }
        .dream-textarea textarea {
            background-color: rgba(255, 255, 255, 0.05);
            color: white;
            border-radius: 10px;
            border: 1px solid #444;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- LOTTIE ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_zoom = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_stars = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_49rdyysj.json")

# --- INTRO SCREEN ---
if 'entered' not in st.session_state:
    st.session_state.entered = False

if not st.session_state.entered:
    st.image("assets/intro_mockup.png", use_container_width=True)
    if st.button("Entrer dans Rêvelia ☁️"):
        st.session_state.entered = True
        time.sleep(1)
        st.rerun()
    st.stop()

# --- TRANSITION ZOOM ---
st_lottie(lottie_zoom, height=250, key="zoom")
time.sleep(1.5)

# --- HEADER ---
st.markdown("<div class='title'>Bienvenue dans Rêvelia</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("📁 Galerie"):
        st.info("Section galerie en construction...")
with col3:
    if st.button("🌙 Morphée"):
        st.info("Section Morphée en construction...")

# --- UPLOAD VOCAL ---
st.markdown("### 🎤 Décris ton rêve")
st_lottie(lottie_stars, height=180, key="stars")
audio_file = st.file_uploader("📂 Charge un rêve en .wav", type=["wav"])

# --- TRAITEMENT COMPLET ---
if audio_file is not None:
    audio_path = Path("temp_audio.wav")
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())

    if st.button("Générer l'image ✨"):
        with st.spinner("🔎 Transcription du rêve..."):
            transcription = get_text_from_audio(audio_path)
        st.success("📄 Rêve transcrit !")
        st.info(transcription)

        with st.spinner("💡 Génération du prompt artistique..."):
            prompt = generate_prompt(transcription)
        st.success("🔹 Prompt généré !")
        st.code(prompt, language="markdown")

        with st.spinner("🎨 Génération de l'image..."):
            output_path = "reve_genere.png"
            clipdrop_key = os.getenv("CLIPDROP_API_KEY")
            generer_image(prompt, clipdrop_key, output_path)

        if os.path.exists(output_path):
            st.image(Image.open(output_path), caption="🎨 Résultat : ton rêve en image")
        else:
            st.error("❌ Image non générée. Vérifie tes crédits ClipDrop.")
