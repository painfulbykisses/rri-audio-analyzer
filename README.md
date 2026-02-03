# 📻 RRI Audio Signal Quality Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

**Digital Audio Signal Quality Analysis Dashboard (Internship Project)**

This application was engineered to facilitate the technical analysis of audio quality from **RRI (Radio Republik Indonesia)** broadcasts, specifically for channels **Pro 1, Pro 2, and Pro 4**. The system utilizes Digital Signal Processing (DSP) techniques to automatically calculate **SNR (Signal-to-Noise Ratio)**, **Noise Floor**, and visualize the **Frequency Spectrum (FFT)**.

---

## 🚀 Method 1: Quick Access (Cloud)

If you want to try the application immediately without installing anything, access the Cloud version deployed via Hugging Face Spaces.

🔗 **Click the link below:**
👉 **https://huggingface.co/spaces/dezikrie/rri-analyzer-audio**

*(The application is accessible via Laptop or Mobile Browsers)*

---

## 💻 Method 2: Running Locally (VS Code)

Follow the steps below if you wish to run the source code on your own local machine.

### 1. Prerequisites
Ensure your computer has the following installed:
* **Python** (Version 3.8 or higher)
* **Visual Studio Code**

### 2. Install Dependencies
Open the **Terminal** in VS Code (`Ctrl + J`), then run the following command to install the required libraries:

```bash
pip install streamlit numpy matplotlib scipy librosa
```

### 3. Run the Application
Once the installation is complete, execute the following command in the Terminal:

```bash
python -m streamlit run app.py
```

Wait a few seconds, and your default web browser will automatically open the application dashboard at http://localhost:8501.

## 🛠️ Key Features
* **Multi-Channel Comparison:** Upload and analyze audio files from RRI Pro 1, Pro 2, and Pro 4 simultaneously.
* **Auto Calculation:** Automatically calculates decibel (dB) values for SNR and Noise Floor.
* **Advanced DSP Filtering:** Utilizes a Bandpass Filter (Butterworth) to separate the clean signal from noise.
* **Data Visualization:**
    * 🌊 **Waveform:** Visualizes amplitude over time (Time Domain).
    * 📊 **FFT Spectrum:** Analyzes frequency distribution (Frequency Domain).
* **Recommendation System:** Provides an automatic conclusion regarding which channel has the best signal quality.

## 🧠 Technical Details (How it Works)

This application uses standard Digital Signal Processing (DSP) logic to separate the "Clean Signal" from "Noise":

### 1. Bandpass Filtering
We apply a **Butterworth Filter (Order 4)** to isolate human voice frequencies.
* **Low Cutoff:** 300 Hz
* **High Cutoff:** 3400 Hz
* **Logic:** Frequencies outside this range are considered "Noise".

### 2. SNR Calculation Formula
The Signal-to-Noise Ratio is calculated using the logarithmic power ratio:

$$SNR_{dB} = 10 \cdot \log_{10} \left( \frac{P_{signal}}{P_{noise}} \right)$$

### 3. FFT (Fast Fourier Transform)
Converts the audio signal from the Time Domain (Amplitude vs Time) to the Frequency Domain (Magnitude vs Hz) to visualize the spectral characteristics.

## 📂 Project Structure

```text
├── app.py              # Main application source code
├── requirements.txt    # Python dependencies list
├── packages.txt        # System-level dependencies (Linux/Debian)
├── README.md           # Project documentation
└── assets/             # Folder containing logos and images
```

## 📝 Author

**Intern Student - RRI Malang 2026**
*Computational Physics Student*
