"""
WhisperMind — Whisper Transcription + Gemini Flash Intelligence
===============================================================
Stack  : Python · OpenAI Whisper · FFmpeg · Streamlit · Gemini Flash
Setup  :
    pip install streamlit openai-whisper sounddevice scipy numpy google-genai python-dotenv
    FFmpeg must be on PATH: https://ffmpeg.org/download.html
    Add SPEECH=your_gemini_api_key to a .env file next to this script
Run    : streamlit run whisper.py
"""

import os
import time
import tempfile

import numpy as np
import scipy.io.wavfile as wav_io
import sounddevice as sd
import streamlit as st
import whisper
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# ─── Constants ────────────────────────────────────────────────────────────────
SAMPLE_RATE        = 16000
CHANNELS           = 1
DURATION           = 5        # seconds to record per press
GEMINI_MODEL       = "gemini-2.5-flash"

GEMINI_MODES = {
    "✨ Smart Summary":        "Summarize the following transcription clearly and concisely in 3-5 bullet points.",
    "🔑 Key Takeaways":        "Extract the most important facts or action items from this transcription as a numbered list.",
    "📝 Clean & Format":       "Rewrite this transcription with proper punctuation, paragraphing, and capitalization. Fix any obvious transcription errors.",
    "🌐 Translate to English": "Translate the following transcription into fluent English. If it is already English, improve the grammar.",
    "❓ Q&A Insights":         "Generate 3 insightful questions and answers based on the content of this transcription.",
    "💬 Casual Rewrite":       "Rewrite this transcription in a friendly, conversational tone suitable for a chat message.",
}

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="WhisperMind", page_icon="🎙️", layout="centered")

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;600&display=swap');

  :root {
    --bg:      #0c0c0e;
    --surface: #131316;
    --border:  rgba(255,255,255,0.07);
    --amber:   #f59e0b;
    --cyan:    #22d3ee;
    --red:     #f87171;
    --text:    #e5e0d8;
    --muted:   #52525b;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
  }
  .stApp {
    background:
      radial-gradient(ellipse 90% 60% at 50% -10%, #1a1106 0%, transparent 55%),
      var(--bg);
    min-height: 100vh;
  }

  /* ── Header ── */
  .masthead-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem;
    letter-spacing: 0.06em;
    color: var(--amber);
    line-height: 1;
    text-shadow: 0 0 40px rgba(245,158,11,0.35);
    margin-bottom: 0;
  }
  .tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.3rem;
    margin-bottom: 2.5rem;
  }

  /* ── Speak button area ── */
  .speak-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1.5rem 0 2rem;
  }
  .mic-ring {
    width: 90px; height: 90px;
    border-radius: 50%;
    background: rgba(245,158,11,0.08);
    border: 2px solid rgba(245,158,11,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 30px rgba(245,158,11,0.15);
    transition: all 0.2s ease;
  }

  /* Countdown ring animation */
  .mic-ring.listening {
    border-color: var(--amber);
    box-shadow: 0 0 0 0 rgba(245,158,11,0.5);
    animation: sonar 1.2s ease-out infinite;
  }
  @keyframes sonar {
    0%   { box-shadow: 0 0 0 0   rgba(245,158,11,0.55); }
    70%  { box-shadow: 0 0 0 22px rgba(245,158,11,0);    }
    100% { box-shadow: 0 0 0 0   rgba(245,158,11,0);     }
  }

  /* ── Countdown bar ── */
  .countdown-track {
    width: 220px;
    height: 3px;
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    margin-top: 0.8rem;
    overflow: hidden;
  }
  .countdown-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--amber), #fde68a);
    border-radius: 99px;
    transition: width 0.1s linear;
  }

  /* ── Transcript box ── */
  .transcript-box {
    background: rgba(245,158,11,0.04);
    border: 1px solid rgba(245,158,11,0.18);
    border-radius: 14px;
    padding: 1.5rem 1.7rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.95rem;
    line-height: 1.85;
    color: #fef3c7;
    white-space: pre-wrap;
    position: relative;
    overflow: hidden;
  }
  .transcript-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--amber), transparent);
  }

  /* ── Gemini box ── */
  .gemini-box {
    background: rgba(34,211,238,0.04);
    border: 1px solid rgba(34,211,238,0.18);
    border-radius: 14px;
    padding: 1.5rem 1.7rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.8;
    color: #cffafe;
    white-space: pre-wrap;
    position: relative;
    overflow: hidden;
  }
  .gemini-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--cyan), transparent);
  }

  /* ── Section label ── */
  .sec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.7rem;
    margin-top: 1.4rem;
  }

  /* ── Pills ── */
  .pill-row { margin-top: 0.8rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
  .pill {
    display: inline-block;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.2rem 0.8rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
  }
  .pill-a { border-color:rgba(245,158,11,0.25); color:#fbbf24; background:rgba(245,158,11,0.06); }
  .pill-c { border-color:rgba(34,211,238,0.25);  color:#67e8f9; background:rgba(34,211,238,0.06); }

  /* ── Divider ── */
  .rule { border:none; border-top:1px solid var(--border); margin:1.6rem 0; }

  /* ── Error box ── */
  .err-box {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: var(--red);
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    margin-top: 0.8rem;
  }

  /* ── History ── */
  .hist-entry {
    padding: 1rem 1.2rem;
    border-left: 2px solid rgba(245,158,11,0.3);
    margin-bottom: 0.9rem;
    background: rgba(255,255,255,0.012);
    border-radius: 0 10px 10px 0;
  }
  .hist-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.35rem;
  }
  .hist-text { font-size: 0.88rem; color: #a8a29e; line-height: 1.6; }

  /* ── Buttons override ── */
  .stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    border: none !important;
    transition: all 0.18s ease !important;
    letter-spacing: 0.02em !important;
  }
  /* Primary speak button */
  .speak-btn .stButton > button {
    background: var(--amber) !important;
    color: #0c0c0e !important;
    font-size: 1.05rem !important;
    padding: 0.75rem 3rem !important;
    box-shadow: 0 0 28px rgba(245,158,11,0.35) !important;
  }
  .speak-btn .stButton > button:hover {
    box-shadow: 0 0 48px rgba(245,158,11,0.6) !important;
    transform: translateY(-2px) !important;
  }
  /* Gemini run */
  .run-btn .stButton > button {
    background: rgba(34,211,238,0.12) !important;
    border: 1px solid rgba(34,211,238,0.3) !important;
    color: var(--cyan) !important;
  }
  .run-btn .stButton > button:hover {
    background: rgba(34,211,238,0.2) !important;
    transform: translateY(-1px) !important;
  }
  /* Clear button */
  .clear-btn .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    padding: 0.4rem 1rem !important;
  }

  .stSelectbox > div > div,
  .stTextArea textarea,
  .stSlider {
    background: rgba(255,255,255,0.04) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
  }
  label { color: var(--muted) !important; font-size: 0.82rem !important; }
  div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
  }
  .streamlit-expanderHeader { color: var(--muted) !important; font-size: 0.82rem !important; }

  /* ── Footer ── */
  .footer {
    margin-top: 3rem;
    padding-top: 1.4rem;
    border-top: 1px solid var(--border);
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #27272a;
    text-align: center;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
</style>
""", unsafe_allow_html=True)

# ─── Session state ────────────────────────────────────────────────────────────
for k, v in [("transcript",""), ("gemini_out",""), ("rec_duration",0.0),
             ("wc",0), ("history",[]), ("listening",False), ("countdown",0)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── API key ──────────────────────────────────────────────────────────────────
api_key = os.getenv("SPEECH")
if not api_key:
    st.markdown('<div class="err-box">⚠️ SPEECH key not found in .env — add <code>SPEECH=your_key</code> and restart.</div>', unsafe_allow_html=True)
    st.stop()

# ─── Load Whisper ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading Whisper…")
def load_whisper_model(size: str):
    return whisper.load_model(size)

# ─── Core functions ───────────────────────────────────────────────────────────
def record_audio(duration: int) -> np.ndarray:
    audio = sd.rec(
        int(SAMPLE_RATE * duration),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
    )
    sd.wait()
    return audio

def transcribe_audio(audio: np.ndarray, model, language=None) -> str:
    audio_int16 = (audio * 32767).astype(np.int16)
    # On Windows, the file must be closed before Whisper (FFmpeg) can read it.
    # Using delete=False + explicit close + manual unlink avoids WinError 32.
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        wav_io.write(tmp.name, SAMPLE_RATE, audio_int16)
        tmp.close()                      # release the handle so FFmpeg can open it
        kwargs = {"fp16": False}
        if language:
            kwargs["language"] = language
        result = model.transcribe(tmp.name, **kwargs)
    finally:
        try:
            os.unlink(tmp.name)          # clean up after Whisper is done
        except OSError:
            pass
    return result["text"].strip()

def run_gemini(transcript: str, mode_prompt: str) -> str:
    client = genai.Client(api_key=api_key)
    full_prompt = f"{mode_prompt}\n\nTranscription:\n{transcript}"
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[types.Part.from_text(text=full_prompt)],
    )
    return response.text.strip()

# ═════════════════════════════════════════════════════
#  UI
# ═════════════════════════════════════════════════════

# ── Header ───────────────────────────────────────────
st.markdown("""
<h1 class="masthead-title">🎙 WHISPERMIND</h1>
<p class="tagline">OpenAI Whisper · FFmpeg · Gemini Flash — speak, transcribe, enhance</p>
""", unsafe_allow_html=True)

# ── Settings ─────────────────────────────────────────
with st.expander("⚙️  Settings", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        model_size = st.selectbox("Whisper model", ["tiny","base","small","medium","large"], index=1)
    with c2:
        duration = st.slider("Recording duration (sec)", 3, 30, 5, 1)
    with c3:
        lang_map = {
            "Auto-detect": None, "English": "en", "Hindi": "hi",
            "Spanish": "es", "French": "fr", "German": "de",
            "Japanese": "ja", "Chinese": "zh",
        }
        lang_label = st.selectbox("Language", list(lang_map.keys()))
        whisper_lang = lang_map[lang_label]

wmodel = load_whisper_model(model_size)

# ── Central mic button ────────────────────────────────
ring_class = "mic-ring listening" if st.session_state.listening else "mic-ring"
fill_pct   = 0 if not st.session_state.listening else int(
    (1 - st.session_state.countdown / duration) * 100
)

st.markdown(f"""
<div class="speak-wrap">
  <div class="{ring_class}">🎙️</div>
</div>
""", unsafe_allow_html=True)

# Centered speak button
col_l, col_m, col_r = st.columns([2, 2, 2])
with col_m:
    st.markdown('<div class="speak-btn">', unsafe_allow_html=True)
    speak_clicked = st.button("🎤  Speak", use_container_width=True, disabled=st.session_state.listening)
    st.markdown('</div>', unsafe_allow_html=True)

# Countdown bar (visible while recording)
if st.session_state.listening:
    st.markdown(f"""
    <div style="display:flex;justify-content:center;margin-top:-0.5rem;margin-bottom:1rem;">
      <div>
        <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#f59e0b;
                    text-align:center;letter-spacing:0.15em;margin-bottom:0.4rem;">
          LISTENING · {st.session_state.countdown}s
        </div>
        <div class="countdown-track">
          <div class="countdown-fill" style="width:{fill_pct}%;"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Clear button (top-right style)
if st.session_state.transcript and not st.session_state.listening:
    col_x, col_y = st.columns([5,1])
    with col_y:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("✕ Clear", use_container_width=True):
            st.session_state.transcript = ""
            st.session_state.gemini_out = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── Handle Speak click ────────────────────────────────
if speak_clicked and not st.session_state.listening:
    st.session_state.listening   = True
    st.session_state.transcript  = ""
    st.session_state.gemini_out  = ""
    st.session_state.countdown   = duration
    st.rerun()

# ── Countdown + record loop ───────────────────────────
if st.session_state.listening:
    if st.session_state.countdown > 0:
        # Show live countdown ticking down
        if st.session_state.countdown == duration:
            # First tick — start the actual recording in this pass
            with st.spinner(""):
                audio = record_audio(duration)
            # Recording done; transcribe immediately
            with st.spinner("🔬  Transcribing…"):
                try:
                    text = transcribe_audio(audio, wmodel, language=whisper_lang)
                    st.session_state.transcript     = text
                    st.session_state.rec_duration   = duration
                    st.session_state.wc             = len(text.split())
                except Exception as e:
                    st.session_state.transcript = f"[Whisper error: {e}]"
            st.session_state.listening  = False
            st.session_state.countdown  = 0
            st.rerun()
        else:
            time.sleep(1)
            st.session_state.countdown -= 1
            st.rerun()

# ── Transcript output ─────────────────────────────────
if st.session_state.transcript:
    st.markdown('<div class="sec-label">✦ Transcript</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="pill-row">'
        f'<span class="pill pill-a">⏱ {st.session_state.rec_duration}s</span>'
        f'<span class="pill pill-a">📝 {st.session_state.wc} words</span>'
        f'<span class="pill">Whisper {model_size}</span>'
        f'<span class="pill">FFmpeg</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.text_area("📋 Copy", value=st.session_state.transcript, height=80, key="_cp_raw")

    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    # ── Gemini Flash section ──────────────────────────
    st.markdown('<div class="sec-label">⚡ Gemini Flash</div>', unsafe_allow_html=True)

    ga, gb = st.columns([3, 1])
    with ga:
        mode = st.selectbox("Mode", list(GEMINI_MODES.keys()), label_visibility="collapsed")
    with gb:
        st.markdown('<div class="run-btn">', unsafe_allow_html=True)
        run_clicked = st.button("⚡ Run", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if run_clicked:
        with st.spinner("Gemini thinking…"):
            try:
                out = run_gemini(st.session_state.transcript, GEMINI_MODES[mode])
                st.session_state.gemini_out = out
                st.session_state.history.insert(0, {
                    "transcript": st.session_state.transcript,
                    "gemini":     out,
                    "mode":       mode,
                    "duration":   st.session_state.rec_duration,
                    "words":      st.session_state.wc,
                })
            except Exception as e:
                st.session_state.gemini_out = f"[Gemini error: {e}]"
        st.rerun()

    if st.session_state.gemini_out:
        st.markdown(f'<div class="gemini-box">{st.session_state.gemini_out}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="pill-row">'
            f'<span class="pill pill-c">🤖 {GEMINI_MODEL}</span>'
            f'<span class="pill pill-c">{mode}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.text_area("📋 Copy Gemini output", value=st.session_state.gemini_out, height=80, key="_cp_gem")

# ── History ───────────────────────────────────────────
if st.session_state.history:
    with st.expander(f"📜  History ({len(st.session_state.history)})", expanded=False):
        for i, e in enumerate(st.session_state.history):
            st.markdown(f"""
            <div class="hist-entry">
              <div class="hist-meta">#{i+1} · {e['duration']}s · {e['words']} words · {e['mode']}</div>
              <div class="hist-text"><b>Transcript:</b> {e['transcript']}</div>
              <div class="hist-text" style="margin-top:0.35rem;color:#71717a;">
                <b>Gemini:</b> {e['gemini'][:300]}{'…' if len(e['gemini'])>300 else ''}
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────
st.markdown(
    '<div class="footer">OpenAI Whisper · FFmpeg · Gemini Flash · Streamlit · Python</div>',
    unsafe_allow_html=True,
)