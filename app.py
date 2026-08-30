import math
import time
import threading
from collections import deque

import av
import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, VideoProcessorBase

st.set_page_config(page_title="AETHRIX | Drowsiness Monitor", page_icon="🚗", layout="wide", initial_sidebar_state="expanded")

# ---------- Styling ----------
st.markdown("""
<style>
:root { --bg:#07111f; --panel:#0d1b2f; --panel2:#12243d; --line:#203956; --text:#f3f7fb; --muted:#91a4bc; --cyan:#38c7ff; --green:#45e39a; --amber:#ffc857; --red:#ff6262; }
.stApp { background: radial-gradient(circle at 10% 0%, #102b49 0%, #07111f 36%, #07111f 100%); color:var(--text); }
.block-container { padding-top: 1.2rem; max-width: 1250px; }
.hero { padding: 24px 28px; border:1px solid var(--line); border-radius:24px; background:linear-gradient(135deg,rgba(18,36,61,.95),rgba(8,22,39,.95)); margin-bottom:18px; }
.brand { color:var(--cyan); font-size:14px; font-weight:800; letter-spacing:2px; }
.hero h1 { margin:.2rem 0 .35rem 0; font-size:36px; }
.hero p { color:var(--muted); margin:0; font-size:16px; }
.card { border:1px solid var(--line); border-radius:18px; background:rgba(13,27,47,.9); padding:18px; min-height:110px; }
.label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:1px; font-weight:700; }
.value { color:var(--text); font-size:24px; font-weight:800; margin-top:8px; }
.small { color:var(--muted); font-size:13px; margin-top:4px; }
.section { color:var(--cyan); font-weight:800; letter-spacing:1px; font-size:13px; margin:20px 0 10px; }
.info-card { border-left:4px solid var(--cyan); padding:13px 16px; background:rgba(18,36,61,.7); border-radius:12px; color:#dce8f5; }
.map-card { text-align:center; padding:18px 8px; border:1px solid var(--line); border-radius:16px; background:rgba(18,36,61,.65); }
.map-icon { font-size:28px; }
.map-title { font-weight:800; margin-top:7px; }
.map-sub { color:var(--muted); font-size:12px; margin-top:3px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ---------- Math helpers ----------
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def ratio(points, idx):
    p = [points[i] for i in idx]
    return (dist(p[1], p[5]) + dist(p[2], p[4])) / (2.0 * max(dist(p[0], p[3]), 1e-6))

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [61, 81, 13, 291, 178, 402]

class DrowsinessProcessor(VideoProcessorBase):
    def __init__(self):
        self.mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True,
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.lock = threading.Lock()
        self.ear_history = deque(maxlen=120)
        self.mar_history = deque(maxlen=120)
        self.head_history = deque(maxlen=120)
        self.baseline_ear_samples = deque(maxlen=120)
        self.baseline_mar_samples = deque(maxlen=120)
        self.baseline_head_samples = deque(maxlen=120)
        self.baseline_ear = None
        self.baseline_mar = None
        self.baseline_head = None
        self.calibrating = False
        self.calibration_started = 0.0
        self.closed_frames = 0
        self.yawn_frames = 0
        self.risk = 0
        self.status = "NO FACE"
        self.reason = "Waiting for driver"
        self.last_face = False

    def calibrate(self):
        with self.lock:
            self.baseline_ear = None
            self.baseline_mar = None
            self.baseline_head = None
            self.baseline_ear_samples.clear(); self.baseline_mar_samples.clear(); self.baseline_head_samples.clear()
            self.closed_frames = 0; self.yawn_frames = 0; self.risk = 0
            self.status = "CALIBRATING"
            self.reason = "Look straight and stay relaxed for a few seconds"
            self.calibrating = True
            self.calibration_started = time.time()

    def get_state(self):
        with self.lock:
            return {
                "ear": self.ear_history[-1] if self.ear_history else 0,
                "mar": self.mar_history[-1] if self.mar_history else 0,
                "head": self.head_history[-1] if self.head_history else 0,
                "baseline_ear": self.baseline_ear,
                "baseline_mar": self.baseline_mar,
                "baseline_head": self.baseline_head,
                "risk": self.risk,
                "status": self.status,
                "reason": self.reason,
                "calibrating": self.calibrating,
                "closed_frames": self.closed_frames,
                "last_face": self.last_face,
            }

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.mesh.process(rgb)

        if result.multi_face_landmarks:
            face = result.multi_face_landmarks[0]
            h, w = img.shape[:2]
            pts = [(lm.x * w, lm.y * h) for lm in face.landmark]

            current_ear = (ratio(pts, LEFT_EYE) + ratio(pts, RIGHT_EYE)) / 2
            current_mar = ratio(pts, MOUTH)
            # Simple normalized head-position cue: nose relative to midpoint of eyes.
            eye_mid_x = (pts[33][0] + pts[263][0]) / 2
            eye_mid_y = (pts[33][1] + pts[263][1]) / 2
            face_width = max(dist(pts[33], pts[263]), 1)
            head_offset = math.hypot((pts[1][0] - eye_mid_x) / face_width, (pts[1][1] - eye_mid_y) / face_width)

            with self.lock:
                self.last_face = True
                self.ear_history.append(current_ear); self.mar_history.append(current_mar); self.head_history.append(head_offset)

                if self.calibrating:
                    self.baseline_ear_samples.append(current_ear)
                    self.baseline_mar_samples.append(current_mar)
                    self.baseline_head_samples.append(head_offset)
                    if len(self.baseline_ear_samples) >= 60 or (time.time() - self.calibration_started) > 8:
                        self.baseline_ear = float(np.median(self.baseline_ear_samples)) if self.baseline_ear_samples else 0.28
                        self.baseline_mar = float(np.median(self.baseline_mar_samples)) if self.baseline_mar_samples else 0.35
                        self.baseline_head = float(np.median(self.baseline_head_samples)) if self.baseline_head_samples else head_offset
                        self.calibrating = False

                ear_base = self.baseline_ear or 0.28
                mar_base = self.baseline_mar or 0.35
                head_base = self.baseline_head or 0.15

                eye_closed = current_ear < max(0.18, ear_base * 0.80)
                yawning = current_mar > max(0.52, mar_base * 1.45)
                head_abnormal = abs(head_offset - head_base) > 0.12

                if eye_closed: self.closed_frames += 1
                else: self.closed_frames = max(0, self.closed_frames - 2)
                if yawning: self.yawn_frames += 1
                else: self.yawn_frames = max(0, self.yawn_frames - 1)

                eye_component = min(55, self.closed_frames * 1.8)
                yawn_component = min(25, self.yawn_frames * 1.2)
                head_component = 12 if head_abnormal else 0
                persistence = 15 if self.closed_frames >= 12 else 0
                self.risk = int(min(100, eye_component + yawn_component + head_component + persistence))

                if self.calibrating:
                    self.status = "CALIBRATING"; self.reason = "Learning your normal facial pattern"
                elif self.risk >= 70:
                    self.status = "DROWSY RISK"; self.reason = "Sustained abnormal cues detected"
                elif self.risk >= 35:
                    self.status = "ALERT"; self.reason = "Early fatigue cues detected"
                else:
                    self.status = "NORMAL"; self.reason = "No sustained drowsiness pattern"

                if self.status == "DROWSY RISK":
                    cv2.putText(img, "DROWSINESS ALERT", (25, 48), cv2.FONT_HERSHEY_SIMPLEX, .9, (0,0,255), 3)
                elif self.status == "ALERT":
                    cv2.putText(img, "STAY ALERT", (25, 48), cv2.FONT_HERSHEY_SIMPLEX, .9, (0,165,255), 3)
                else:
                    cv2.putText(img, "DRIVER MONITORED", (25, 48), cv2.FONT_HERSHEY_SIMPLEX, .8, (255,255,255), 2)
                cv2.putText(img, f"Risk {self.risk}%", (25, 82), cv2.FONT_HERSHEY_SIMPLEX, .65, (255,255,255), 2)
        else:
            with self.lock:
                self.last_face = False; self.status = "NO FACE"; self.reason = "Move into camera view"; self.risk = 0
            cv2.putText(img, "FACE NOT DETECTED", (25, 48), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,165,255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="brand">AETHRIX • SMART INDIA HACKATHON</div>
  <h1>Adaptive Driver Drowsiness Risk Monitoring</h1>
  <p>Real-time computer-vision prototype • Python • OpenCV • MediaPipe</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎛️ Demo Control")
    st.markdown("**1.** Start camera and allow permission.  \n**2.** Sit straight and look at the camera.  \n**3.** Click **Calibrate Baseline**.  \n**4.** Demonstrate prolonged eye closure/yawning.")
    st.divider()
    st.markdown("### 🧠 Detection Logic")
    st.caption("Personalized baseline")
    st.caption("Multi-cue analysis")
    st.caption("Time-based adaptive risk")
    st.divider()
    st.caption("Prototype demonstration only — not a certified driving-safety device.")

RTC = RTCConfiguration({"iceServers": []})
ctx = webrtc_streamer(
    key="aethrix-drowsiness-v2", mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC, media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=DrowsinessProcessor, async_processing=True
)

if ctx.video_processor:
    if st.button("🎯 Calibrate Driver Baseline", use_container_width=True):
        ctx.video_processor.calibrate()

    @st.fragment(run_every="1s")
    def live_dashboard():
        state = ctx.video_processor.get_state()

        status = state["status"]

        status_icon = {
            "NORMAL": "🟢",
            "ALERT": "🟡",
            "DROWSY RISK": "🔴",
            "CALIBRATING": "🔵",
            "NO FACE": "⚪"
        }.get(status, "⚪")

        st.markdown(
            '<div class="section">LIVE DRIVER STATUS</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.markdown(
            f'<div class="card"><div class="label">Driver Status</div>'
            f'<div class="value">{status_icon} {status}</div>'
            f'<div class="small">{state["reason"]}</div></div>',
            unsafe_allow_html=True
        )

        c2.markdown(
            f'<div class="card"><div class="label">Risk Score</div>'
            f'<div class="value">{state["risk"]}%</div>'
            f'<div class="small">Adaptive time-based score</div></div>',
            unsafe_allow_html=True
        )

        c3.markdown(
            f'<div class="card"><div class="label">Eye Ratio (EAR)</div>'
            f'<div class="value">{state["ear"]:.2f}</div>'
            f'<div class="small">Eye closure indicator</div></div>',
            unsafe_allow_html=True
        )

        c4.markdown(
            f'<div class="card"><div class="label">Mouth Ratio</div>'
            f'<div class="value">{state["mar"]:.2f}</div>'
            f'<div class="small">Yawning indicator</div></div>',
            unsafe_allow_html=True
        )

        st.progress(state["risk"] / 100)

        if status == "DROWSY RISK":  
            st.error("🚨 DROWSINESS RISK — Trigger driver warning.")
            st.audio("alert.wav", format="audio/wav", autoplay=True)
        elif status == "ALERT":
            st.warning("⚠️ EARLY FATIGUE CUES — Stay alert.")
        elif status == "CALIBRATING":
            st.info("🔵 CALIBRATING — Keep a normal, relaxed face for a few seconds.")
        elif status == "NORMAL":
            st.success("✅ DRIVER OK — No sustained drowsiness pattern detected.")
        else:
            st.info("ℹ️ Position your face inside the camera view.")

        st.markdown(
            '<div class="section">MULTI-CUE SIGNALS</div>',
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)

        a.markdown(
            '<div class="card"><div class="label">01 • Eyes</div>'
            '<div class="value">👁️ Blink / Closure</div>'
            '<div class="small">EAR-based eye behaviour</div></div>',
            unsafe_allow_html=True
        )

        b.markdown(
            '<div class="card"><div class="label">02 • Mouth</div>'
            '<div class="value">🥱 Yawning</div>'
            '<div class="small">Mouth-opening behaviour</div></div>',
            unsafe_allow_html=True
        )

        c.markdown(
            '<div class="card"><div class="label">03 • Head</div>'
            '<div class="value">🧑 Head Behaviour</div>'
            '<div class="small">Normalized head-position cue</div></div>',
            unsafe_allow_html=True
        )

    live_dashboard()

else:
    st.info("📷 Start the camera above to begin the live prototype.")

st.markdown(
    '<div class="section">PROTOTYPE → FUTURE DEPLOYMENT</div>',
    unsafe_allow_html=True
)

cols = st.columns(5)

items = [
    ("📷", "CAMERA", "Laptop webcam"),
    ("👤", "DETECTION", "MediaPipe landmarks"),
    ("🧠", "RISK ENGINE", "Baseline + multi-cue + time"),
    ("📊", "DASHBOARD", "Laptop web interface"),
    ("🚗", "FUTURE", "Vehicle camera + edge device")
]

for col, (icon, title, sub) in zip(cols, items):
    with col:
        st.markdown(
            f'<div class="map-card">'
            f'<div class="map-icon">{icon}</div>'
            f'<div class="map-title">{title}</div>'
            f'<div class="map-sub">{sub}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown(
    '<div class="info-card">💡 <b>Judge-ready explanation:</b> '
    'The laptop is the prototype environment. The core detection and '
    'risk-assessment pipeline is what we validate here; future deployment '
    'moves that software pipeline to vehicle-facing camera and edge hardware.'
    '</div>',
    unsafe_allow_html=True
)