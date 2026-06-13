import cv2
import time
import streamlit as st

from modules.hand_tracking import HandTracker
from modules.gesture_logic import GestureRecognizer
from modules.speech import Speaker
from modules.sentence_builder import SentenceBuilder

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HandSign AI",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #080c10 !important;
    color: #e2e8f0;
    font-family: 'Syne', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
footer { display: none; }
.block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px;
}

/* ── scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 4px; }

/* ── top nav bar ── */
.hs-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 2.5rem 0;
    border-bottom: 1px solid #0e1e2e;
    margin-bottom: 2.5rem;
}
.hs-logo {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #e2e8f0;
}
.hs-logo span {
    color: #38bdf8;
}
.hs-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    color: #38bdf8;
    background: #0c1e2e;
    border: 1px solid #1e3a5f;
    padding: 4px 10px;
    border-radius: 4px;
}

/* ── section titles ── */
.hs-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* ── camera card ── */
.hs-cam-card {
    background: #0d1117;
    border: 1px solid #0e1e2e;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
}
.hs-cam-topbar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-bottom: 1px solid #0e1e2e;
    background: #0a0e14;
}
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.dot-r { background: #ef4444; }
.dot-y { background: #f59e0b; }
.dot-g { background: #22c55e; }
.cam-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #475569;
    margin-left: 6px;
}
[data-testid="stImage"] img {
    border-radius: 0 0 12px 12px !important;
    width: 100% !important;
    display: block;
}

/* ── status indicator ── */
.hs-live-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
}
.hs-live-active {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.25);
    color: #4ade80;
}
.hs-live-inactive {
    background: rgba(100,116,139,0.08);
    border: 1px solid rgba(100,116,139,0.2);
    color: #64748b;
}
.pulse {
    width: 7px; height: 7px; border-radius: 50%;
    display: inline-block;
    animation: pulse 1.6s ease-in-out infinite;
}
.pulse-green { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
.pulse-gray { background: #64748b; animation: none; }
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── detected word card ── */
.hs-word-card {
    background: #0d1117;
    border: 1px solid #0e1e2e;
    border-radius: 12px;
    padding: 28px 24px;
    margin-bottom: 16px;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hs-word-empty {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #1e3a5f;
    letter-spacing: 1px;
}
.hs-word-detected {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #38bdf8;
    line-height: 1;
}
.hs-sentence {
    font-size: 16px;
    color: #94a3b8;
    margin-top: 8px;
    font-weight: 400;
}

/* ── stat cards row ── */
.hs-stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.hs-stat {
    background: #0d1117;
    border: 1px solid #0e1e2e;
    border-radius: 10px;
    padding: 16px 18px;
}
.hs-stat-val {
    font-size: 26px;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1;
}
.hs-stat-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #334155;
    text-transform: uppercase;
    margin-top: 6px;
}

/* ── gesture legend ── */
.hs-legend {
    background: #0d1117;
    border: 1px solid #0e1e2e;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 16px;
}
.hs-legend-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #0a0e14;
}
.hs-legend-row:last-child { border-bottom: none; }
.hs-legend-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #38bdf8;
    font-weight: 500;
    min-width: 90px;
}
.hs-legend-fingers {
    display: flex;
    gap: 5px;
}
.finger {
    width: 14px; height: 22px;
    border-radius: 3px 3px 2px 2px;
    border: 1px solid #1e3a5f;
}
.finger-up { background: #38bdf8; border-color: #38bdf8; }
.finger-down { background: #0d1117; border-color: #1e3a5f; }
.hs-legend-phrase {
    font-size: 12px;
    color: #475569;
    font-style: italic;
}

/* ── history log ── */
.hs-log {
    background: #0d1117;
    border: 1px solid #0e1e2e;
    border-radius: 12px;
    padding: 16px 20px;
}
.hs-log-entry {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #0a0e14;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
.hs-log-entry:last-child { border-bottom: none; }
.hs-log-word { color: #38bdf8; }
.hs-log-time { color: #1e3a5f; font-size: 11px; }

/* ── toggle button ── */
div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid #1e3a5f !important;
    color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    padding: 6px 18px !important;
    border-radius: 6px !important;
    transition: all 0.2s;
}
div[data-testid="stButton"] > button:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
    background: rgba(56,189,248,0.05) !important;
}

/* ── checkbox start/stop ── */
[data-testid="stCheckbox"] label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #64748b;
    letter-spacing: 1px;
}

/* ── hide default streamlit chrome ── */
#MainMenu { display: none; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────────
if "init" not in st.session_state:
    st.session_state.tracker = HandTracker()
    st.session_state.gesture = GestureRecognizer()
    st.session_state.speaker = Speaker()
    st.session_state.builder = SentenceBuilder()

    st.session_state.prev = ""
    st.session_state.time = 0
    st.session_state.text = ""
    st.session_state.sentence = ""
    st.session_state.count = 0
    st.session_state.session_words = []
    st.session_state.log = []  # list of (word, timestamp_str)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    st.session_state.cap = cap
    st.session_state.init = True

tracker  = st.session_state.tracker
gesture  = st.session_state.gesture
speaker  = st.session_state.speaker
builder  = st.session_state.builder
cap      = st.session_state.cap

# ── Nav bar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hs-nav">
  <div class="hs-logo">Hand<span>Sign</span> AI</div>
  <div style="display:flex;align-items:center;gap:14px;">
    <div class="hs-badge">v1.0.0</div>
    <div class="hs-badge">ASSISTIVE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    st.markdown('<div class="hs-section-label">Live Feed</div>', unsafe_allow_html=True)

    # Camera chrome wrapper top
    st.markdown("""
    <div class="hs-cam-card">
      <div class="hs-cam-topbar">
        <span class="dot dot-r"></span>
        <span class="dot dot-y"></span>
        <span class="dot dot-g"></span>
        <span class="cam-label">CAM_0 · 640×480 · BGR</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    frame_box = st.empty()

    # Controls row
    ctrl_l, ctrl_r = st.columns([1, 1])
    with ctrl_l:
        run = st.checkbox("▶  START CAMERA", value=True)
    with ctrl_r:
        if st.button("CLEAR LOG"):
            st.session_state.log = []
            st.session_state.count = 0
            st.session_state.session_words = []
            st.session_state.text = ""
            st.session_state.sentence = ""

with right:
    # ── Live status ──────────────────────────────────────────────────────────
    st.markdown('<div class="hs-section-label">Status</div>', unsafe_allow_html=True)
    status_box = st.empty()

    # ── Detected word ────────────────────────────────────────────────────────
    st.markdown('<div class="hs-section-label" style="margin-top:20px;">Detected Gesture</div>', unsafe_allow_html=True)
    word_box = st.empty()

    # ── Stats row ────────────────────────────────────────────────────────────
    st.markdown('<div class="hs-section-label" style="margin-top:20px;">Session Stats</div>', unsafe_allow_html=True)
    stats_box = st.empty()

    # ── Gesture legend ───────────────────────────────────────────────────────
    st.markdown('<div class="hs-section-label" style="margin-top:20px;">Gesture Map</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hs-legend">
      <div class="hs-legend-row">
        <span class="hs-legend-name">FOOD</span>
        <span class="hs-legend-fingers">
          <span class="finger finger-down"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-down"></span>
          <span class="finger finger-down"></span>
        </span>
        <span class="hs-legend-phrase">"Please give me food"</span>
      </div>
      <div class="hs-legend-row">
        <span class="hs-legend-name">WATER</span>
        <span class="hs-legend-fingers">
          <span class="finger finger-down"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-down"></span>
        </span>
        <span class="hs-legend-phrase">"I need water"</span>
      </div>
      <div class="hs-legend-row">
        <span class="hs-legend-name">MEDICINE</span>
        <span class="hs-legend-fingers">
          <span class="finger finger-down"></span>
          <span class="finger finger-down"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-up"></span>
        </span>
        <span class="hs-legend-phrase">"I need medicine"</span>
      </div>
      <div class="hs-legend-row">
        <span class="hs-legend-name">REST</span>
        <span class="hs-legend-fingers">
          <span class="finger finger-down"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-up"></span>
          <span class="finger finger-up"></span>
        </span>
        <span class="hs-legend-phrase">"I want to rest"</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── History log ──────────────────────────────────────────────────────────
    st.markdown('<div class="hs-section-label" style="margin-top:20px;">History Log</div>', unsafe_allow_html=True)
    log_box = st.empty()


# ── Helper renderers ───────────────────────────────────────────────────────────
def render_status(active: bool):
    if active:
        status_box.markdown("""
        <div class="hs-live-indicator hs-live-active">
          <span class="pulse pulse-green"></span> LIVE · HAND TRACKING ACTIVE
        </div>""", unsafe_allow_html=True)
    else:
        status_box.markdown("""
        <div class="hs-live-indicator hs-live-inactive">
          <span class="pulse pulse-gray"></span> STANDBY · CAMERA OFF
        </div>""", unsafe_allow_html=True)


def render_word(word, sentence):
    if word:
        word_box.markdown(f"""
        <div class="hs-word-card">
          <div class="hs-word-detected">{word}</div>
          <div class="hs-sentence">{sentence}</div>
        </div>""", unsafe_allow_html=True)
    else:
        word_box.markdown("""
        <div class="hs-word-card">
          <div class="hs-word-empty">— awaiting gesture —</div>
        </div>""", unsafe_allow_html=True)


def render_stats(count, words):
    unique = len(set(words)) if words else 0
    last = words[-1] if words else "—"
    stats_box.markdown(f"""
    <div class="hs-stats-row">
      <div class="hs-stat">
        <div class="hs-stat-val">{count}</div>
        <div class="hs-stat-lbl">Total Signs</div>
      </div>
      <div class="hs-stat">
        <div class="hs-stat-val">{unique}</div>
        <div class="hs-stat-lbl">Unique</div>
      </div>
      <div class="hs-stat">
        <div class="hs-stat-val" style="font-size:18px;color:#38bdf8">{last}</div>
        <div class="hs-stat-lbl">Last Word</div>
      </div>
    </div>""", unsafe_allow_html=True)


def render_log(log_entries):
    if not log_entries:
        log_box.markdown("""
        <div class="hs-log">
          <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#1e3a5f;letter-spacing:1px;">
            — no entries yet —
          </div>
        </div>""", unsafe_allow_html=True)
        return
    rows = ""
    for word, ts in reversed(log_entries[-8:]):
        rows += f"""
        <div class="hs-log-entry">
          <span class="hs-log-word">{word}</span>
          <span class="hs-log-time">{ts}</span>
        </div>"""
    log_box.markdown(f'<div class="hs-log">{rows}</div>', unsafe_allow_html=True)


# ── Initial renders ────────────────────────────────────────────────────────────
render_status(run)
render_word(st.session_state.text, st.session_state.sentence)
render_stats(st.session_state.count, st.session_state.session_words)
render_log(st.session_state.log)

# ── Main loop ──────────────────────────────────────────────────────────────────
delay = 0.5

while run:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame, lm = tracker.find_hands(frame)
    g = gesture.recognize(lm)

    if g != "":
        if g == st.session_state.prev:
            if time.time() - st.session_state.time > delay:
                if st.session_state.text != g:
                    st.session_state.text = g
                    sentence = builder.build(g)
                    if sentence:
                        st.session_state.sentence = sentence
                        speaker.speak(sentence)
                        st.session_state.count += 1
                        st.session_state.session_words.append(g)
                        ts = time.strftime("%H:%M:%S")
                        st.session_state.log.append((g, ts))
        else:
            st.session_state.prev = g
            st.session_state.time = time.time()
    else:
        st.session_state.prev = ""
        st.session_state.time = 0

    frame_box.image(frame, channels="BGR", use_container_width=True)
    render_word(st.session_state.text, st.session_state.sentence)
    render_stats(st.session_state.count, st.session_state.session_words)
    render_log(st.session_state.log)

    time.sleep(0.02)

render_status(False)
