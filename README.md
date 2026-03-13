# 🏋️ AI Real-Time Pose Trainer

A desktop application that uses your webcam to analyze exercise form in real time and provides instant corrective feedback using computer vision and AI.

## ✨ Features

- 🎯 Real-time pose detection using MediaPipe (33 body landmarks)
- 📐 Joint angle calculation and comparison against ideal form
- 🔢 Automatic rep counting per exercise
- 💯 Live accuracy score (0–100) per frame
- 🔴🟢 Color-coded skeleton overlay (green = correct, red = needs correction)
- 🔊 Voice feedback via text-to-speech
- 💬 On-screen correction messages (e.g. "Keep your back straight")
- 🔄 Switch between exercises instantly with keyboard shortcuts

---

## 🏃 Exercises Included

| Exercise | Joints Tracked |
|----------|---------------|
| Squat | Knees, Back angle |
| Bicep Curl | Elbow, Shoulder |
| Push-up | Elbow, Body alignment |
| Shoulder Press | Elbow, Shoulder raise, Torso |

---

## 🛠️ Tech Stack

- **Python 3.10**
- **MediaPipe** — Pose landmark detection
- **OpenCV** — Webcam capture and visual overlay
- **NumPy** — Joint angle calculations
- **pyttsx3** — Offline text-to-speech feedback
