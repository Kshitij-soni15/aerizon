# 🚗 AETHRIX

### Adaptive Driver Drowsiness Risk Monitoring

> **A real-time computer-vision based functional prototype for detecting early signs of driver drowsiness.**

AETHRIX is a **functional AI/computer-vision prototype** that monitors facial behaviour through a webcam and estimates drowsiness risk using multiple behavioural cues.

Instead of relying on a single signal, AETHRIX combines **eye closure, yawning, head behaviour, personalized baseline calibration, and temporal analysis** to generate a continuously updated risk assessment.

---

## ✨ What AETHRIX Does

* 👁️ **Eye Closure Detection** using Eye Aspect Ratio (EAR)
* 🥱 **Yawning Detection** using mouth-opening behaviour
* 🧑 **Head Behaviour Analysis** using facial landmarks
* 🧠 **Personalized Baseline Calibration**
* ⏱️ **Temporal / Persistence Analysis**
* 📊 **Real-Time 0–100% Risk Score**
* 🚨 **Visual & Audio Drowsiness Warning**
* 🎥 **Live Webcam Monitoring**
* 🌐 **Interactive Monitoring Dashboard**

---

## 🧠 How It Works

```text
              📷 CAMERA
                  │
                  ▼
          🎥 VIDEO FRAMES
                  │
                  ▼
        🔍 MEDIAPIPE FACE MESH
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      👁️ EYES   🥱 MOUTH   🧑 HEAD
        │         │         │
       EAR       MAR    HEAD CUE
        └─────────┼─────────┘
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
        ┌─────────┼─────────┐
        ▼         ▼         ▼
     🟢 NORMAL  🟡 ALERT  🔴 DROWSY
                            │
                            ▼
                       🚨 WARNING
```

---

## 🔬 Core Detection Logic

### 👁️ Eye Aspect Ratio — EAR

Facial landmarks around the eyes are used to calculate an eye-opening ratio.

**Lower EAR → increased eye closure**

The system also considers how long the abnormal condition persists rather than reacting to a single frame.

### 🥱 Mouth Aspect Ratio — MAR

Mouth landmarks are used to estimate mouth opening.

**Higher MAR → possible yawning behaviour**

### 🧑 Head Behaviour

The position of facial landmarks is used to calculate a normalized head-position cue.

The observed behaviour is compared against the driver's personalized baseline.

### ⏱️ Temporal Analysis

AETHRIX does not treat every unusual frame as drowsiness.

It accumulates abnormal behaviour over time and increases the risk score when the behaviour persists.

> **Persistent abnormal behaviour → higher drowsiness risk**

---

## 🧠 Adaptive Calibration

Every driver can have slightly different natural facial measurements.

Therefore, AETHRIX includes a **baseline calibration stage**.

The driver looks normally at the camera and selects:

**`Calibrate Driver Baseline`**

The system learns reference values for:

* Eye behaviour
* Mouth behaviour
* Head position

Future observations are then compared against these personalized values.

---

## 🚦 Risk States

| Status             | Meaning                                     |
| ------------------ | ------------------------------------------- |
| 🟢 **NORMAL**      | No sustained drowsiness pattern detected    |
| 🟡 **ALERT**       | Early fatigue-related cues detected         |
| 🔴 **DROWSY RISK** | Sustained abnormal cues detected            |
| 🔵 **CALIBRATING** | Learning the driver's normal facial pattern |
| ⚪ **NO FACE**      | Driver is not detected in the camera view   |

---

## ⚙️ Technology Stack

| Technology           | Role                            |
| -------------------- | ------------------------------- |
| **Python 3.11**      | Core application                |
| **OpenCV**           | Image and video processing      |
| **MediaPipe**        | Facial landmark detection       |
| **NumPy**            | Numerical calculations          |
| **Streamlit**        | Interactive dashboard           |
| **streamlit-webrtc** | Real-time webcam streaming      |
| **PyAV / aiortc**    | Video frame & WebRTC processing |

---

## 🖥️ Prototype Architecture

```text
Laptop Webcam
      │
      ▼
MediaPipe Face Mesh
      │
      ▼
Facial Landmark Extraction
      │
      ▼
EAR + MAR + Head Behaviour
      │
      ▼
Personalized Baseline
      │
      ▼
Temporal Risk Engine
      │
      ▼
Live Risk Score
      │
      ▼
Streamlit Dashboard
      │
      ▼
Visual + Audio Warning
```

---

## 🚀 Run the Prototype

### Requirements

* Windows PC / Laptop
* Python **3.11.x**
* Working webcam
* Internet connection for first-time dependency installation

### Start

Open the project folder and run:

```text
START_AETHRIX.bat
```

The launcher starts the project environment and launches the AETHRIX dashboard.

### Demo Steps

1. Start the camera.
2. Allow camera permission.
3. Sit normally in front of the camera.
4. Click **Calibrate Driver Baseline**.
5. Demonstrate different facial behaviours.
6. Observe the live status and risk score.
7. Demonstrate the warning state.

---

## 🏗️ From Prototype to Real-World Deployment

The current implementation is a **laptop-based functional prototype** designed to validate the core computer-vision and risk-assessment pipeline.

The same software concept can later be adapted to vehicle-oriented hardware.

```text
              CURRENT PROTOTYPE
                     │
             Laptop Webcam
                     │
                     ▼
          Computer Vision Pipeline
                     │
                     ▼
             Risk Assessment
                     │
                     ▼
              Live Dashboard


                     ↓
              FUTURE DEPLOYMENT
                     ↓

          Vehicle-Facing Camera
                     │
                     ▼
             Edge Computing
                     │
                     ▼
          Real-Time Risk Engine
                     │
                     ▼
             Driver Warning
```

### Possible Future Enhancements

* 🚘 Vehicle-facing camera integration
* ⚡ Edge-device deployment
* 🔊 Dedicated in-vehicle warning system
* 📈 Long-term driver behaviour analytics
* 🔗 Integration with vehicle systems

---

## 🔐 Privacy

AETHRIX is designed as a local demonstration prototype.

The application does not require personal documents, academic records, or unrelated files to operate.

---

## ⚠️ Disclaimer

> **AETHRIX is a functional prototype for academic and hackathon demonstration purposes. It is not a certified driving-safety system and should not be relied upon while operating a real vehicle.**

---

## 👨‍💻 Author

### **Kshitij Soni**

**B.Tech Student | AI & Computer Vision**

**Project:** AETHRIX
**Focus:** Real-Time Driver Drowsiness Risk Monitoring

---

## 📌 Project Status

### 🟢 Functional Prototype — Working Demonstration

The current prototype successfully demonstrates the core pipeline:

**Camera → Face Landmarks → Behaviour Analysis → Temporal Risk Assessment → Warning**

---

<div align="center">

### 🚗 AETHRIX

**Detect Early. Assess Continuously. Respond Intelligently.**

*Built for innovation, experimentation & real-world deployment research.*

</div>
