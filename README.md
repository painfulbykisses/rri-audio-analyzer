# 📻 RRI Audio Signal Quality Analyzer

> **Digital Audio Signal Quality Analysis Dashboard**
> Internship Project — LPP RRI Malang 2026

This application analyzes audio quality from **RRI (Radio Republik Indonesia)** broadcasts across channels **Pro 1**, **Pro 2**, and **Pro 4**. Built with a **Flask + HTML/CSS/JS** architecture — Python handles the DSP (Digital Signal Processing) logic while the frontend delivers a modern, dark-themed dashboard experience.

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
- **Python 3.8+** — [Download here](https://www.python.org/downloads/)

### Installation

```bash
# Navigate to your Desktop (or any folder you prefer)
cd %USERPROFILE%\Desktop

# Clone the repository
git clone https://github.com/painfulbykisses/rri-audio-analyzer.git
cd rri-audio-analyzer

# Install Python dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
python server.py
```

Open your browser and navigate to **[http://localhost:5000](http://localhost:5000)**

---

## 📂 Project Structure

```
rri-audio-analyzer/
├── server.py              # Flask backend + DSP logic (API)
├── templates/
│   └── index.html         # Frontend dashboard (HTML/CSS/JS)
├── requirements.txt       # Python dependencies
├── logo_rri.png           # RRI logo
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
| **Chart.js** (CDN) | Frontend chart rendering |

## 📝 Author

**Muhammad Dzikri H.C.H**
Intern Student — RRI Malang 2026
Computational Physics Student
