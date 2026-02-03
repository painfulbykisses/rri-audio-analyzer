import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import librosa

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="RRI Audio Analyzer",
    page_icon="📻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem; }
    [data-testid="stAppViewContainer"] { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e5e7eb; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    h1, h2, h3, h4, p, li, span, div { color: #1f2937; }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E3A8A !important; margin-bottom: 5px; line-height: 1.2; }
    .subtitle { font-size: 1.0rem; color: #64748B !important; font-weight: 400; margin-bottom: 25px; }
    .winner-box { background-color: #F0FDF4; padding: 25px; border-radius: 12px; border: 1px solid #16A34A; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin: 20px 0; }
    .winner-text-head { color: #15803d !important; font-size: 20px; font-weight: 800; margin-bottom: 5px; }
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-size: 1.6rem !important; }
    div[data-testid="stImage"] { display: block; margin-left: auto; margin-right: auto; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIKA DSP
# ==========================================
def bandpass_filter(data, fs, lowcut, highcut, order):
    nyq = 0.5 * fs
    if highcut >= nyq: highcut = nyq - 1
    b, a = butter(order, [lowcut/nyq, highcut/nyq], btype='band')
    return filtfilt(b, a, data)

def calculate_metrics(clean_signal, noise_signal):
    p_signal = np.mean(clean_signal ** 2)
    p_noise = np.mean(noise_signal ** 2)
    if p_noise == 0: snr = 0
    else: snr = 10 * np.log10(p_signal / p_noise)
    rms_noise = np.sqrt(p_noise)
    if rms_noise == 0: floor = -90
    else: floor = 20 * np.log10(rms_noise)
    return snr, floor

def compute_fft(signal, fs):
    N = len(signal)
    fft = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(N, 1/fs)
    return freqs, fft / (np.max(fft) + 1e-10)

def process_audio_data(y, sr, low_cut, high_cut, order):
    try:
        clean = bandpass_filter(y, sr, low_cut, high_cut, order)
        noise = y - clean
        snr, floor = calculate_metrics(clean, noise)
        freqs, fft_val = compute_fft(y, sr)
        time_axis = np.arange(len(y)) / sr
        return {
            "audio": y, "noise": noise, "time": time_axis, 
            "snr": snr, "floor": floor, "freqs": freqs, "fft": fft_val
        }
    except Exception as e:
        return {"error": str(e)}

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    try: st.image("logo_rri.png", width=100)
    except: pass
    
    st.title("Menu Sistem")
    st.info("📂 Mode: Komparasi File")
    
    st.markdown("---")
    st.header("🎛️ Filter DSP")
    LOW_CUT = st.slider("Low Cutoff (Hz)", 0, 1000, 300)
    HIGH_CUT = st.slider("High Cutoff (Hz)", 1000, 10000, 3400)
    FILTER_ORDER = st.slider("Filter Order", 1, 10, 4)

# ==========================================
# 4. HALAMAN UTAMA (KOMPARASI FILE)
# ==========================================
st.markdown('<div class="main-title">Komparasi Kualitas Audio (File)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dashboard Komparasi Kualitas Audio Digital (Pro 1 vs Pro 2 vs Pro 4) - Laporan PKL</div>', unsafe_allow_html=True)

results = {}
col1, col2, col3 = st.columns(3)
COLOR_MAP = {"RRI Pro 1": "#DC2626", "RRI Pro 2": "#D97706", "RRI Pro 4": "#059669"}

def render_upload(col, title, key, logo):
    with col:
        with st.container(border=True):
            st.markdown(f"#### {title}")
            uploaded = st.file_uploader(f"Up {title}", type=['mp3', 'wav'], key=key, label_visibility="collapsed")
            if uploaded:
                y, sr = librosa.load(uploaded, sr=None, mono=True)
                data = process_audio_data(y, sr, LOW_CUT, HIGH_CUT, FILTER_ORDER)
                st.metric("SNR Quality", f"{data['snr']:.2f} dB")
                st.audio(uploaded)
                return {title: data}
    return None

r1 = render_upload(col1, "RRI Pro 1", "u1", "pro 1.png")
r2 = render_upload(col2, "RRI Pro 2", "u2", "pro 2.png")
r3 = render_upload(col3, "RRI Pro 4", "u4", "pro 4.png")

if r1: results.update(r1)
if r2: results.update(r2)
if r3: results.update(r3)

if results:
    st.divider()
    best_ch = max(results, key=lambda x: results[x]['snr'])
    st.markdown(f"""
    <div class="winner-box">
        <div class="winner-text-head">🏆 REKOMENDASI: {best_ch}</div>
        <div>SNR Tertinggi: <b>{results[best_ch]['snr']:.2f} dB</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    gc1, gc2, gc3 = st.columns(3)
    def plot_graph(col, title, data):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                plt.style.use('default')
                DS_WAVE, DS_FFT = 100, 10
                
                fig1, ax1 = plt.subplots(figsize=(5, 2))
                ax1.plot(data['time'][::DS_WAVE], data['audio'][::DS_WAVE], color='#1E3A8A', alpha=0.5)
                ax1.plot(data['time'][::DS_WAVE], data['noise'][::DS_WAVE], color='red', alpha=0.6)
                ax1.set_xticks([]); ax1.set_ylabel("Amp")
                fig1.patch.set_alpha(0); st.pyplot(fig1)
                
                fig2, ax2 = plt.subplots(figsize=(5, 2))
                c = COLOR_MAP.get(title, "blue")
                ax2.plot(data['freqs'][::DS_FFT], data['fft'][::DS_FFT], color=c)
                ax2.fill_between(data['freqs'][::DS_FFT], data['fft'][::DS_FFT], color=c, alpha=0.3)
                ax2.set_xlim(0, 5000); ax2.set_xlabel("Hz")
                fig2.patch.set_alpha(0); st.pyplot(fig2)

    if "RRI Pro 1" in results: plot_graph(gc1, "RRI Pro 1", results["RRI Pro 1"])
    if "RRI Pro 2" in results: plot_graph(gc2, "RRI Pro 2", results["RRI Pro 2"])
    if "RRI Pro 4" in results: plot_graph(gc3, "RRI Pro 4", results["RRI Pro 4"])
