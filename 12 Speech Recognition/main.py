# Speech Recognition using Google Gemini API
"""
Setup Instructions:
1. pip install streamlit SpeechRecognition pyaudio google-genai python-dotenv
2. Get your Gemini API key from: https://aistudio.google.com/app/apikey
3. Add SPEECH=your_api_key to a .env file in the same directory.
4. Run: streamlit run speech_recognition_gemini.py
"""

import io
import os
import time
import wave
import tempfile
import streamlit as st
import speech_recognition as spreg
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Loads SPEECH (and other vars) from .env file

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VoiceScribe — Gemini Powered",
    page_icon="🎙️",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

  html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background: #0a0a0f;
    color: #e8e4dc;
  }

  .stApp {
    background: radial-gradient(ellipse at 20% 10%, #1a0a2e 0%, #0a0a0f 60%);
    min-height: 100vh;
  }

  h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0 !important;
  }

  .subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #6b7280;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
  }

  /* API key input section */
  .api-section {
    background: rgba(167, 139, 250, 0.06);
    border: 1px solid rgba(167, 139, 250, 0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
  }

  /* Settings panel */
  .settings-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  /* Result box */
  .result-box {
    background: rgba(52, 211, 153, 0.05);
    border: 1px solid rgba(52, 211, 153, 0.25);
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #34d399, #60a5fa, #a78bfa);
  }
  .result-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #34d399;
    margin-bottom: 0.8rem;
  }
  .result-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    line-height: 1.7;
    color: #f0ece4;
  }

  /* Error box */
  .error-box {
    background: rgba(239, 68, 68, 0.06);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    color: #fca5a5;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
  }

  /* Stats row */
  .stat-pill {
    display: inline-block;
    background: rgba(96, 165, 250, 0.1);
    border: 1px solid rgba(96, 165, 250, 0.2);
    border-radius: 999px;
    padding: 0.25rem 0.9rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #93c5fd;
    margin-right: 0.5rem;
    margin-top: 0.8rem;
  }

  /* Streamlit overrides */
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 24px rgba(124, 58, 237, 0.35) !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 40px rgba(124, 58, 237, 0.55) !important;
  }

  .stTextInput > div > div > input,
  .stSelectbox > div > div,
  .stSlider {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e8e4dc !important;
    border-radius: 8px !important;
  }
  label { color: #9ca3af !important; font-size: 0.85rem !important; }

  div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
  }
  .streamlit-expanderHeader { color: #9ca3af !important; }
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("<h1>🎙️ VoiceScribe</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Gemini Flash · Long-form · High Accuracy</p>', unsafe_allow_html=True)


# ─── Session State ───────────────────────────────────────────────────────────
if "transcript_history" not in st.session_state:
    st.session_state.transcript_history = []


# ─── API Key from .env ────────────────────────────────────────────
api_key = os.getenv("SPEECH")
if not api_key:
    st.markdown('<div class="error-box">⚠️ SPEECH key not found in .env — add <code>SPEECH=your_key</code> and restart.</div>', unsafe_allow_html=True)
    st.stop()


# ─── Settings ───────────────────────────────────────────────────────────────
with st.expander("⚙️ Recording & Model Settings", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        phrase_limit = st.slider("Max recording duration (sec)", 10, 120, 30, 5)
        silence_timeout = st.slider("Silence timeout (sec)", 3, 15, 7)
    with col2:
        language_options = {
            "English (India)": "en-IN",
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "Hindi": "hi-IN",
            "Spanish": "es-ES",
            "French": "fr-FR",
            "German": "de-DE",
            "Japanese": "ja-JP",
        }
        selected_lang_label = st.selectbox("🌐 Hint Language", list(language_options.keys()))
        selected_lang = language_options[selected_lang_label]

        model_choice = st.selectbox(
            "🤖 Gemini Model",
            ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-3.1-pro-preview"],
            index=0,
            help="2.5 Pro = best accuracy. 2.5 Flash = fast & efficient. 3.1 Pro Preview = latest flagship."
        )

    gemini_prompt = st.text_area(
        "📝 Transcription prompt (optional)",
        value="Please transcribe the following audio accurately. Preserve punctuation and formatting.",
        height=80,
        help="Guide Gemini with context about the audio content for better results."
    )


# ─── Core Functions ──────────────────────────────────────────────────────────
def record_audio(timeout: int, phrase_limit: int) -> bytes | None:
    """Record audio from microphone and return raw WAV bytes."""
    recog = spreg.Recognizer()
    recog.energy_threshold = 400
    recog.dynamic_energy_threshold = True
    recog.pause_threshold = 0.8
    recog.non_speaking_duration = 0.5

    try:
        with spreg.Microphone(sample_rate=16000) as source:
            recog.adjust_for_ambient_noise(source, duration=1)
            audio = recog.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit,
            )
        # Convert to WAV bytes
        wav_bytes = audio.get_wav_data()
        return wav_bytes
    except spreg.WaitTimeoutError:
        return None
    except Exception as e:
        raise RuntimeError(f"Microphone error: {e}")


def transcribe_with_gemini(wav_bytes: bytes, api_key: str, model_name: str, prompt: str, lang_hint: str) -> dict:
    """Send WAV audio to Gemini and return transcription + metadata."""
    
    # 1. Initialize the new genai Client
    client = genai.Client(api_key=api_key)

    # Write to a temp file — Gemini SDK needs a file path or inline data
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(wav_bytes)
        tmp_path = tmp.name

    try:
        # 2. Upload audio file using client.files
        audio_file = client.files.upload(file=tmp_path)

        # 3. Wait until file is active
        for _ in range(10):
            file_status = client.files.get(name=audio_file.name)
            if file_status.state.name == "ACTIVE":
                break
            time.sleep(1)

        full_prompt = f"{prompt}\n\nLanguage hint: {lang_hint}"
        
        # 4. Generate content using client.models
        response = client.models.generate_content(
            model=model_name,
            contents=[full_prompt, audio_file]
        )

        # 5. Cleanup uploaded file
        client.files.delete(name=audio_file.name)

        # Extract word count and duration estimate from wav
        with wave.open(io.BytesIO(wav_bytes), 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = round(frames / float(rate), 1)

        text = response.text.strip()
        word_count = len(text.split())
        return {"text": text, "duration": duration, "words": word_count, "model": model_name}

    finally:
        os.unlink(tmp_path)


# ─── Main Button ─────────────────────────────────────────────────────────────
col_btn, col_clear = st.columns([3, 1])
with col_btn:
    record_clicked = st.button("🎙️ Start Recording", use_container_width=True)
with col_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.transcript_history = []
        st.rerun()

if record_clicked:
    if not api_key:
        st.markdown('<div class="error-box">⚠️ Please enter your Gemini API key above.</div>', unsafe_allow_html=True)
    else:
        # Step 1 — Record
        with st.spinner("🎧 Listening… speak now!"):
            try:
                wav_bytes = record_audio(timeout=silence_timeout, phrase_limit=phrase_limit)
            except RuntimeError as e:
                st.markdown(f'<div class="error-box">🎤 {e}</div>', unsafe_allow_html=True)
                wav_bytes = None

        if wav_bytes is None:
            st.markdown('<div class="error-box">⏱️ No speech detected within the timeout window. Try again.</div>', unsafe_allow_html=True)
        else:
            # Step 2 — Transcribe
            with st.spinner(f"🤖 Transcribing with {model_choice}…"):
                try:
                    result = transcribe_with_gemini(
                        wav_bytes,
                        api_key=api_key,
                        model_name=model_choice,
                        prompt=gemini_prompt,
                        lang_hint=selected_lang,
                    )

                    # Save to history
                    st.session_state.transcript_history.insert(0, result)

                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Gemini API error: {e}</div>', unsafe_allow_html=True)
                    result = None

            # Step 3 — Display latest result
            if result:
                st.markdown(f"""
                <div class="result-box">
                  <div class="result-label">✦ Transcription</div>
                  <div class="result-text">{result['text']}</div>
                  <div>
                    <span class="stat-pill">⏱ {result['duration']}s recorded</span>
                    <span class="stat-pill">📝 {result['words']} words</span>
                    <span class="stat-pill">🤖 {result['model']}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Copy button via text area
                st.text_area("📋 Copy text", value=result["text"], height=100, key="copy_area")


# ─── History ─────────────────────────────────────────────────────────────────
if len(st.session_state.transcript_history) > 1:
    with st.expander(f"📜 Previous transcripts ({len(st.session_state.transcript_history) - 1} earlier)", expanded=False):
        for i, entry in enumerate(st.session_state.transcript_history[1:], 1):
            st.markdown(f"""
            <div style="padding: 1rem; border-left: 2px solid rgba(167,139,250,0.3); margin-bottom: 1rem;">
              <span style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#6b7280; text-transform:uppercase; letter-spacing:0.15em;">
                #{i} · {entry['duration']}s · {entry['words']} words
              </span>
              <p style="margin: 0.4rem 0 0; font-size:0.95rem; color:#d1cdc7;">{entry['text']}</p>
            </div>
            """, unsafe_allow_html=True)


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.06);
     font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #374151; text-align: center; letter-spacing: 0.1em;">
  GEMINI AUDIO API · UP TO 8.4 HRS AUDIO · MULTI-LANGUAGE
</div>
""", unsafe_allow_html=True)