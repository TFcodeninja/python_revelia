import streamlit as st
from pathlib import Path
from PIL import Image
from whisper_transcribe import get_text_from_audio
from mistral_prompt_generator import generate_prompt
from clipdrop_generator import generer_image
import sounddevice as sd
import soundfile as sf
import tempfile
import requests
from streamlit_lottie import st_lottie
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Rêvelia", page_icon="🌙", layout="centered")

# CSS personnalisé pour un thème premium bleu nuit
def inject_custom_css():
    st.markdown("""
        <style>
        /* Fond général en dégradé bleu nuit */
        html, body, [class*="css"] {
            background: linear-gradient(to bottom, #001f3f, #00112e) !important;
            color: #0F056B !important;
            font-family: 'Segoe UI', sans-serif;
        }
        /* En-tête transparent pour laisser voir le dégradé */
        .stHeader, .st-bv, .css-1v3fvcr, .css-10trblm {
            background-color: transparent !important;
        }
        /* Textareas semi-transparents */
        .stTextArea>div>div>textarea {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #0F056B !important;
            border-radius: 8px !important;
            border: 1px solid #005f99 !important;
        }
        /* Boutons primaires bleu foncé avec légers reflets */
        .stButton>button {
            background-color: #005f99 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5em 1.2em !important;
            font-weight: 600 !important;
            transition: background-color 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #004f7a !important;
        }
        /* Titres centrés avec couleur bleue claire */
        .block-title {
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5em;
            color: #6ba8e5 !important;
        }
        /* Pied de page sobre */
        footer {
            color: #0F056B !important;
            text-align: center;
            margin-top: 3em;
        }
        /* Colormap pour les selectbox et slider */
        .stSelectbox>div>div>div>div {
            background-color: rgba(13, 4, 116, 1) !important;
            color: #0F056B !important;
        }
        .stSlider>div>div>div>input {
            accent-color: #6ba8e5 !important;
        }
        /* Info et alertes stylées */
        .stInfo, .stSuccess, .stError, .stWarning {
            border-radius: 8px !important;
            padding: 0.5em 1em !important;
        }
        .stInfo .stText, .stSuccess .stText, .stError .stText, .stWarning .stText {
            color: #0F056B !important;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# Charger animations Lottie
@st.cache_data
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Placeholder Lottie URLs remain, but we'll overlay static images instead
lottie_zoom = load_lottie("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_stars = load_lottie("https://assets1.lottiefiles.com/packages/lf20_49rdyysj.json")

# Initialisation de l'état de session
if 'entered' not in st.session_state:
    st.session_state.entered = False
if 'section' not in st.session_state:
    st.session_state.section = 'home'
if 'gallery' not in st.session_state:
    st.session_state.gallery = []
if 'recorded_audio_path' not in st.session_state:
    st.session_state.recorded_audio_path = None
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

# Écran d'introduction avec image de lune sur fond bleu nuit
if not st.session_state.entered:
    st.markdown("""
        <div style='text-align: center; padding-top: 50px;'>
            <img src='https://i.pinimg.com/736x/90/a1/26/90a1264a19f0dfec3c94a3549ea92969.jpg' 
                 width='250' style='border-radius: 50%; border: 2px solid #6ba8e5;' />
            <h1 class='block-title'>Rêvelia</h1>
            <p style='color: 	#0F056B;'>Explorez et visualisez vos rêves</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Entrer dans Rêvelia ☁️"):
        st.session_state.entered = True
        st.rerun()
    st.stop()

# Transition Zoom (overlay d'image de ciel étoilé sur fond bleu nuit)
if lottie_zoom:
    st_lottie(lottie_zoom, height=250, key="zoom")
else:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuRYmmKqU38pcXFeUEGW_VsS08pb2nD3EGmpNE366Fa4ZbiCqVSB5tdgVsRFZ1qk7Sl-w&usqp=CAU", use_container_width=True)

# Barre latérale de navigation
st.sidebar.title("Menu")
section = st.sidebar.radio("Aller à", ["Accueil", "Galerie", "Morphée"])
st.session_state.section = section.lower()

# --- Section Accueil ---
if st.session_state.section == "accueil":
    st.markdown("<h2 class='block-title'>Bienvenue dans Rêvelia</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: 	#0F056B;'>Décrivez votre rêve et voyez-le prendre vie</p>", unsafe_allow_html=True)

    # Afficher une image de nuages sur fond bleu nuit
    st.image("https://m1.quebecormedia.com/emp/emp/dream688102f1-03d1-42cf-9cd8-e8d154868fb0_ORIGINAL.jpg?impolicy=crop-resize&x=0&y=0&w=0&h=0&width=925", use_container_width=True)

    st.subheader("🎤 Étape 1 : Fournissez votre rêve")
    audio_input = st.radio("Méthode d'entrée audio", ["Uploader un fichier", "Enregistrer maintenant"])

    # Si l’utilisateur choisit d’uploader
    if audio_input == "Uploader un fichier":
        uploaded_file = st.file_uploader("Téléverser un fichier audio (.wav ou .mp3)", type=["wav", "mp3"])
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                st.session_state.recorded_audio_path = tmp.name
            st.audio(st.session_state.recorded_audio_path)
    # Si l’utilisateur choisit d’enregistrer en direct
    else:
        # Le slider va maintenant jusqu’à 30 secondes
        duration = st.slider("Durée de l'enregistrement (secondes)", 3, 30, 10)
        # Bouton pour démarrer/arrêter l'enregistrement
        if not st.session_state.is_recording:
            if st.button("🎤 Enregistrer le rêve"):
                st.session_state.is_recording = True
        if st.session_state.is_recording:
            with st.spinner("Enregistrement en cours..."):
                fs = 44100
                recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
                sd.wait()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    sf.write(tmp.name, recording, fs)
                    st.session_state.recorded_audio_path = tmp.name
                st.session_state.is_recording = False
                st.success("Enregistrement terminé ")
                st.audio(st.session_state.recorded_audio_path)

    # Étape 2 : Génération
    if st.session_state.recorded_audio_path:
        st.subheader("✨ Étape 2 : Génération du rêve visuel")
        style = st.selectbox("Choisissez un style d'image", ["onirique", "surréaliste", "absurde", "mystique"])
        if st.button("Générer l'image "):
            with st.spinner("Analyse et génération en cours..."):
                try:
                    transcription = get_text_from_audio(st.session_state.recorded_audio_path)
                    st.markdown(f"**Transcription :** {transcription}")
                    prompt = generate_prompt(transcription)
                    styled_prompt = f"Style {style} : {prompt}"
                    output_path = "reve_genere.png"
                    clipdrop_key = os.getenv("CLIPDROP_API_KEY")
                    generer_image(styled_prompt, clipdrop_key, output_path)

                    if Path(output_path).exists():
                        image = Image.open(output_path)
                        st.image(image, caption="Votre rêve visualisé", use_container_width=True)
                        st.session_state.gallery.append(output_path)
                        st.success("Rêve généré et ajouté à la galerie !")
                    else:
                        st.error(" Image non générée. Vérifiez vos crédits ClipDrop.")
                except Exception as e:
                    st.error(f"Une erreur est survenue : {e}")

# --- Section Galerie ---
elif st.session_state.section == "galerie":
    st.markdown("<h2 class='block-title'>Galerie de Rêves</h2>", unsafe_allow_html=True)
    if st.session_state.gallery:
        for idx, path in enumerate(reversed(st.session_state.gallery)):
            try:
                st.image(Image.open(path), caption=f"Rêve #{len(st.session_state.gallery) - idx}", use_container_width=True)
            except Exception as e:
                st.warning(f"Impossible d'afficher l'image : {e}")
    else:
        st.info("Aucun rêve généré pour l'instant. Commencez par l'accueil !")

# --- Section Morphée ---
elif st.session_state.section == "morphée":
    st.markdown("<h2 class='block-title'>Morphée - Analyse de rêve</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaaaaa;'>Analysez vos rêves et découvrez leur signification</p>", unsafe_allow_html=True)
    reve = st.text_area("Décrivez votre rêve ici...")
    if st.button("Analyser mon rêve "):
        st.info("Cette fonctionnalité est en cours de développement...")

# --- Footer ---
st.markdown("""
    <hr style='margin-top: 3em;' />
    <footer>Rêvelia ©️ 2025 - Explorez vos rêves</footer>
""", unsafe_allow_html=True)
