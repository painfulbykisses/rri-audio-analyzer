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
👉 **[INSERT YOUR HUGGING FACE SPACE LINK HERE]**

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
