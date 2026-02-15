import os
import io
import json
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from scipy.signal import butter, filtfilt
import librosa

# ==========================================
# FLASK APP SETUP
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))
CORS(app)

# ==========================================
# DSP FUNCTIONS (preserved from original app.py)
# ==========================================

def bandpass_filter(data, fs, lowcut, highcut, order):
    """Apply Butterworth bandpass filter to isolate human voice frequencies."""
    nyq = 0.5 * fs
    if highcut >= nyq:
        highcut = nyq - 1
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return filtfilt(b, a, data)


def calculate_metrics(clean_signal, noise_signal):
    """Calculate SNR (dB) and Noise Floor (dB)."""
    p_signal = np.mean(clean_signal ** 2)
    p_noise = np.mean(noise_signal ** 2)
    if p_noise == 0:
        snr = 0
    else:
        snr = 10 * np.log10(p_signal / p_noise)
    rms_noise = np.sqrt(p_noise)
    if rms_noise == 0:
        floor = -90
    else:
        floor = 20 * np.log10(rms_noise)
    return snr, floor


def compute_fft(signal, fs):
    """Compute FFT and return normalized magnitude spectrum."""
    N = len(signal)
    fft = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(N, 1 / fs)
    return freqs, fft / (np.max(fft) + 1e-10)


def process_audio(file_bytes, filename, low_cut=300, high_cut=3400, filter_order=4):
    """Full DSP pipeline: load audio → filter → metrics → FFT."""
    try:
        y, sr = librosa.load(io.BytesIO(file_bytes), sr=None, mono=True)

        # Bandpass filter & metrics
        clean = bandpass_filter(y, sr, low_cut, high_cut, filter_order)
        noise = y - clean
        snr, floor = calculate_metrics(clean, noise)

        # FFT
        freqs, fft_val = compute_fft(y, sr)
        time_axis = np.arange(len(y)) / sr

        # Downsample for JSON transfer (keep charts lightweight)
        DS_WAVE = max(1, len(y) // 2000)
        DS_FFT = max(1, len(freqs) // 1000)

        # Limit FFT to 5000 Hz for display
        freq_mask = freqs <= 5000
        freqs_display = freqs[freq_mask]
        fft_display = fft_val[freq_mask]
        DS_FFT_display = max(1, len(freqs_display) // 1000)

        return {
            "name": filename,
            "snr": round(float(snr), 2),
            "floor": round(float(floor), 2),
            "sample_rate": int(sr),
            "duration": round(float(len(y) / sr), 2),
            "waveform": {
                "time": time_axis[::DS_WAVE].tolist(),
                "audio": y[::DS_WAVE].tolist(),
                "noise": noise[::DS_WAVE].tolist()
            },
            "fft": {
                "freqs": freqs_display[::DS_FFT_display].tolist(),
                "magnitude": fft_display[::DS_FFT_display].tolist()
            },
            "error": None
        }
    except Exception as e:
        return {"error": str(e)}


# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    """Serve the main dashboard page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint: analyze uploaded audio file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Get filter parameters from form data (with defaults)
    low_cut = int(request.form.get('low_cut', 300))
    high_cut = int(request.form.get('high_cut', 3400))
    filter_order = int(request.form.get('filter_order', 4))

    file_bytes = file.read()
    result = process_audio(file_bytes, file.filename, low_cut, high_cut, filter_order)

    if result.get("error"):
        return jsonify(result), 500

    return jsonify(result)


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve logo and image assets from root directory."""
    return send_from_directory(BASE_DIR, filename)


# ==========================================
# RUN
# ==========================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n📻 RRI Audio Signal Quality Analyzer")
    print("=" * 40)
    print(f"🌐 Open in browser: http://localhost:{port}")
    print("=" * 40 + "\n")
    app.run(debug=False, host='0.0.0.0', port=port)
