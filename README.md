---
title: RRI Audio Analyzer
emoji: 📻
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# 📻 RRI Audio Signal Quality Analyzer

> **Digital Audio Signal Quality Analysis Dashboard**
> Internship Project — LPP RRI Malang 2026

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Hugging_Face_Spaces-blue?style=for-the-badge)](https://huggingface.co/spaces/dezikrie/rri-analyzer-audio)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)

This application analyzes audio quality from **RRI (Radio Republik Indonesia)** broadcasts across channels **Pro 1**, **Pro 2**, and **Pro 4**. Built with a **Flask + HTML/CSS/JS** architecture — Python handles the DSP (Digital Signal Processing) logic while the frontend delivers a modern, dark-themed dashboard experience.

🔗 **Live Demo:** [https://huggingface.co/spaces/dezikrie/rri-analyzer-audio](https://huggingface.co/spaces/dezikrie/rri-analyzer-audio)

---

## 🖥️ Architecture

```
┌──────────────────────────┐       ┌──────────────────────────┐
│     Frontend (Browser)   │       │    Backend (Python)       │
│                          │       │                           │
│  HTML / CSS / JavaScript │◄─────►│  Flask API Server         │
│  Chart.js Visualizations │ JSON  │  DSP Processing (NumPy,   │
│  Drag & Drop Upload      │       │  SciPy, Librosa)          │
│  Dark Theme Dashboard    │       │                           │
└──────────────────────────┘       └──────────────────────────┘
```

## 🛠️ Key Features

- **Multi-Channel Comparison** — Upload and analyze audio from RRI Pro 1, Pro 2, and Pro 4 simultaneously
- **Auto Calculation** — Automatically calculates SNR (dB) and Noise Floor (dB)
- **Advanced DSP Filtering** — Butterworth Bandpass Filter (configurable order & cutoff)
- **Interactive Visualizations** — Chart.js powered Waveform and FFT Spectrum charts
- **Recommendation System** — Automatic conclusion on which channel has the best signal quality
- **Modern Dark UI** — Premium glassmorphism design with gradient accents and micro-animations
- **Drag & Drop Upload** — Drag audio files directly onto upload cards

## 🧠 Technical Details (How it Works)

### 1. Bandpass Filtering
Butterworth Filter (Order 4) isolates human voice frequencies:
- **Low Cutoff:** 300 Hz
- **High Cutoff:** 3400 Hz
- Frequencies outside this range are considered "Noise"

### 2. SNR Calculation Formula
$$SNR_{dB} = 10 \cdot \log_{10} \left( \frac{P_{signal}}{P_{noise}} \right)$$

### 3. FFT (Fast Fourier Transform)
Converts audio from Time Domain (Amplitude vs Time) to Frequency Domain (Magnitude vs Hz)

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+** — [Download here](https://www.python.org/downloads/)

### Installation

```bash
# Navigate to your Desktop (or any folder you prefer)
cd ~/Desktop

# Clone the repository
git clone https://github.com/painfulbykisses/rri-audio-analyzer.git
cd rri-audio-analyzer

# Install Python dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
python server.py
```

Open your browser and navigate to **[http://localhost:5000](http://localhost:5000)**

---

## � Docker Deployment

This project includes a Dockerfile for containerized deployment (used by Hugging Face Spaces):

```bash
docker build -t rri-audio-analyzer .
docker run -p 7860:7860 rri-audio-analyzer
```

---

## �📂 Project Structure

```
rri-audio-analyzer/
├── server.py              # Flask backend + DSP logic (API)
├── index.html             # Frontend dashboard (HTML/CSS/JS)
├── Dockerfile             # Docker config for HF Spaces deployment
├── requirements.txt       # Python dependencies
├── package.json           # Project metadata
├── .gitattributes         # Git LFS configuration
├── logo_rri.png           # RRI logo
├── favicon.png            # Browser tab favicon
├── pro 1.png              # Channel Pro 1 icon
├── pro 2.png              # Channel Pro 2 icon
├── pro 4.png              # Channel Pro 4 icon
└── README.md              # This file
```

## 🔧 Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web server & API endpoints |
| `flask-cors` | Cross-origin resource sharing |
| `numpy` | Numerical computations |
| `scipy` | Signal processing (Butterworth filter) |
| `librosa` | Audio file loading & processing |
| `gunicorn` | Production WSGI server |
| **Chart.js** (CDN) | Frontend chart rendering |

## 🌐 Deployment

This app is deployed on **Hugging Face Spaces** using Docker SDK:

🔗 **[https://huggingface.co/spaces/dezikrie/rri-analyzer-audio](https://huggingface.co/spaces/dezikrie/rri-analyzer-audio)**

## 📝 Author

**Muhammad Dzikri H.C.H**
Intern Student — LPP RRI Malang 2026
Computational Physics Student
