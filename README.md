# 🚗 AETHRIX

## Adaptive Driver Drowsiness Risk Monitoring

> **A real-time computer-vision based functional prototype for detecting early signs of driver drowsiness.**

**AETHRIX** monitors facial behaviour through a webcam and estimates drowsiness risk using multiple behavioural cues.

It combines **eye closure, yawning, head behaviour, personalized calibration, and temporal analysis** to provide a continuously updated risk assessment.

---

## ✨ KEY HIGHLIGHTS

|    👁️ Eye Analysis   |  🥱 Yawning Detection  |  🧑 Head Behaviour  |
| :-------------------: | :--------------------: | :-----------------: |
| EAR-based eye closure | Mouth-opening analysis | Facial landmark cue |

|   🧠 Adaptive Baseline   |  ⏱️ Temporal Analysis  |   🚨 Smart Warning   |
| :----------------------: | :--------------------: | :------------------: |
| Personalized calibration | Persistence-based risk | Visual + audio alert |

---

# 🧠 HOW IT WORKS

```text
             📷 CAMERA
                 │
                 ▼
          🎥 VIDEO FRAMES
                 │
                 ▼
       🔍 MEDIAPIPE FACE MESH
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
      👁️ EYES  🥱 MOUTH  🧑 HEAD
        │        │        │
       EAR      MAR    HEAD CUE
        └────────┼────────┘
                 │
                 ▼
        🧠 ADAPTIVE BASELINE
                 │
                 ▼
        ⏱️ TEMPORAL ANALYSIS
                 │
                 ▼
          📊 RISK ENGINE
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
     🟢 NORMAL 🟡 ALERT 🔴 DROWSY
                           │
                           ▼
                      🚨 WARNING
```

---

# 🔬 DETECTION ENGINE

### 👁️ Eye Aspect Ratio — EAR

Facial landmarks around the eyes are used to calculate an eye-opening ratio.

**Lower EAR → increased eye closure**

The system also considers the persistence of eye closure instead of reacting to a single frame.

### 🥱 Mouth Aspect Ratio — MAR

Mouth landmarks are used to estimate mouth opening.

**Higher MAR → possible yawning behaviour**

### 🧑 Head Behaviour

Facial landmarks are used to calculate a normalized head-position cue.

The observed behaviour is compared with the driver's personalized baseline.

### ⏱️ Temporal Analysis

AETHRIX does not immediately classify one unusual frame as drowsiness.

Abnormal behaviour is accumulated over time.

> **Persistent abnormal behaviour → higher drowsiness risk**

---

# 🧠 ADAPTIVE CALIBRATION

Different drivers naturally have different facial measurements.

AETHRIX therefore establishes a **personalized baseline** before monitoring.

### Calibration Flow

```text
Normal Driver Behaviour
          ↓
   Collect Facial Data
          ↓
     Calculate Baseline
          ↓
   Compare Future Cues
          ↓
      Risk Assessment
```

The baseline includes:

* Eye behaviour
* Mouth behaviour
* Head position

---

# 🚦 RISK STATES

| Status             | Meaning                          |
| ------------------ | -------------------------------- |
| 🟢 **NORMAL**      | No sustained drowsiness pattern  |
| 🟡 **ALERT**       | Early fatigue-related cues       |
| 🔴 **DROWSY RISK** | Sustained abnormal cues          |
| 🔵 **CALIBRATING** | Learning normal facial behaviour |
| ⚪ **NO FACE**      | Driver not detected              |

---

# ⚙️ TECHNOLOGY STACK

| Technology           | Purpose                    |
| -------------------- | -------------------------- |
| **Python 3.11**      | Core application           |
| **OpenCV**           | Image & video processing   |
| **MediaPipe**        | Facial landmark detection  |
| **NumPy**            | Numerical calculations     |
| **Streamlit**        | Interactive dashboard      |
| **streamlit-webrtc** | Real-time webcam streaming |
| **PyAV / aiortc**    | Video & WebRTC processing  |

---

# 🖥️ PROTOTYPE ARCHITECTURE

```text
       📷 LAPTOP WEBCAM
              │
              ▼
      MEDIAPIPE FACE MESH
              │
              ▼
    FACIAL LANDMARK EXTRACTION
              │
              ▼
      EAR + MAR + HEAD CUE
              │
              ▼
      PERSONALIZED BASELINE
              │
              ▼
       TEMPORAL RISK ENGINE
              │
              ▼
        LIVE RISK SCORE
              │
              ▼
       STREAMLIT DASHBOARD
              │
              ▼
       🚨 DRIVER WARNING
```

---

# 🚀 RUN THE PROTOTYPE

### Requirements

* Windows PC / Laptop
* Python **3.11.x**
* Working webcam
* Internet connection for first-time setup

### Start

Run:

```text
START_AETHRIX.bat
```

The launcher starts the project environment and opens the AETHRIX dashboard.

### Demo Flow

**01** → Start camera
**02** → Allow camera permission
**03** → Sit normally in front of camera
**04** → Click **Calibrate Driver Baseline**
**05** → Demonstrate facial behaviours
**06** → Observe live risk score
**07** → Demonstrate warning state

---

# 🏗️ PROTOTYPE → FUTURE DEPLOYMENT

The current system is a **laptop-based functional prototype** used to validate the core detection and risk-assessment pipeline.

### CURRENT

```text
Laptop Camera
     ↓
Computer Vision
     ↓
Risk Assessment
     ↓
Live Dashboard
```

### FUTURE

```text
Vehicle-Facing Camera
          ↓
    Edge Computing
          ↓
   Real-Time Engine
          ↓
    Driver Warning
```

### Future Enhancements

* 🚘 Vehicle-facing camera integration
* ⚡ Edge-device deployment
* 🔊 Dedicated in-vehicle warning system
* 📈 Long-term driver behaviour analytics
* 🔗 Vehicle-system integration

---

# 🔐 PRIVACY

AETHRIX is designed as a **local demonstration prototype**.

The application does not require personal documents, academic records, or unrelated files to operate.

---

# ⚠️ DISCLAIMER

> **AETHRIX is a functional prototype for academic and hackathon demonstration purposes. It is not a certified driving-safety system and should not be relied upon while operating a real vehicle.**

---

# 👨‍💻 AUTHOR

## Kshitij Soni

**B.Tech Student · AI & Computer Vision**

**Project:** AETHRIX
**Focus:** Real-Time Driver Drowsiness Risk Monitoring

---

# 📌 PROJECT STATUS

### 🟢 Functional Prototype — Working Demonstration

The current prototype demonstrates the complete core pipeline:

**Camera → Face Landmarks → Behaviour Analysis → Temporal Risk Assessment → Warning**

---

<div align="center">

# 🚗 AETHRIX

### **Detect Early. Assess Continuously. Respond Intelligently.**

*Built for innovation, experimentation & real-world deployment research.*

</div>
