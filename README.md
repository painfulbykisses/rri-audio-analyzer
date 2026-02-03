# 📻 RRI Audio Signal Quality Analyzer

**Digital Audio Signal Quality Analysis Dashboard (Internship Project)**

This application was developed to facilitate the technical analysis of audio quality from **RRI Pro 1, Pro 2, and Pro 4** broadcasts. The system automatically calculates **SNR (Signal-to-Noise Ratio)** and **Noise Floor** values, while providing frequency spectrum visualizations (FFT) to compare signal quality across different channels.

---

## 🚀 Method 1: Quick Access (Cloud)

If you want to try the application immediately without installing anything on your computer, you can access the Cloud version deployed via Hugging Face Spaces.

🔗 **Click the link below:**
👉 **[INSERT YOUR HUGGING FACE SPACE LINK HERE]**

_(The application is accessible via Laptop or Mobile Browsers)_

---

## 💻 Method 2: Running Locally (VS Code)

Follow the steps below if you wish to run the source code on your own local machine.

### 1. Prerequisites
Ensure your computer has the following installed:
- **Python** (Version 3.8 or higher)
- **Visual Studio Code**

### 2. Install Dependencies
Open the **Terminal** in VS Code (`Ctrl + J`), then run the following command to install the required libraries:

```bash
pip install streamlit numpy matplotlib scipy librosa
