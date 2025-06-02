from pathlib import Path
from clipdrop_generator import pipeline_audio_vers_image

audio_path = Path(__file__).parent / "Grouv.wav"
pipeline_audio_vers_image(audio_path)
