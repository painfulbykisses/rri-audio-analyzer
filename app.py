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

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .block-container { padding-top: 5rem !important; padding-bottom: 2rem; }
    [data-testid="stAppViewContainer"] { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #e5e7eb; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    h1, h2, h3, h4, p, li, span, div { color: #1f2937; }
    
    .main-title {
        font-size: 2.5rem; font-weight: 800; color: #1E3A8A !important;
        margin-bottom: 5px; line-height: 1.2;
    }
    .subtitle {
        font-size: 1.1rem; color: #64748B !important;
        font-weight: 400; margin-bottom: 25px;
    }
    
    .winner-box {
        background-color: #F0FDF4; padding: 25px;
        border-radius: 12px; border: 1px solid #16A34A;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin: 20px 0;
    }
    .winner-text-head {
        color: #15803d !important; font-size: 20px; font-weight: 800; margin-bottom: 5px;
    }
    
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-size: 1.6rem !important; }
    div[data-testid="stImage"] { display: block; margin-left: auto; margin-right: auto; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HEADER
# ==========================================
col_logo, col_text = st.columns([1, 5])
with col_logo:
    try: st.image("logo_rri.png", width=130) 
    except: st.error("Logo 404")
with col_text:
    st.markdown('<div class="main-title">RRI Signal Quality Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Dashboard Komparasi Kualitas Audio Digital (Pro 1 vs Pro 2 vs Pro 4) - Laporan PKL</div>', unsafe_allow_html=True)

st.divider()

# ==========================================
# 3. FUNGSI LOGIKA DSP
# ==========================================
with st.sidebar:
    st.header("🎛️ Control Panel")
    st.info("Pengaturan Filter Digital")
    LOW_CUT = st.slider("Low Cutoff (Hz)", 0, 1000, 300)
    HIGH_CUT = st.slider("High Cutoff (Hz)", 1000, 10000, 3400)
    FILTER_ORDER = st.slider("Filter Order", 1, 10, 4)
    st.caption("Developed with Python & Streamlit")

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

def process_audio(uploaded_file):
    if uploaded_file is not None:
        try:
            # Load audio
            y, sr = librosa.load(uploaded_file, sr=None, mono=True)
            
            # Filter & Metrics
            clean = bandpass_filter(y, sr, LOW_CUT, HIGH_CUT, FILTER_ORDER)
            noise = y - clean
            snr, floor = calculate_metrics(clean, noise)
            
            # FFT
            freqs, fft_val = compute_fft(y, sr)
            time_axis = np.arange(len(y)) / sr
            
            return {
                "name": uploaded_file.name, "audio": y, "noise": noise, 
                "time": time_axis, "snr": snr, "floor": floor, 
                "freqs": freqs, "fft": fft_val, "error": None
            }
        except Exception as e:
            return {"error": str(e)}
    return None

# ==========================================
# 4. AREA UPLOAD
# ==========================================
results = {}
col1, col2, col3 = st.columns(3)

COLOR_MAP = {
    "RRI Pro 1": "#DC2626", 
    "RRI Pro 2": "#D97706", 
    "RRI Pro 4": "#059669" 
}

def render_upload_clean(column, title, key, logo_filename):
    with column:
        with st.container(border=True):
            # Header Kecil
            c_img, c_txt = st.columns([1, 3])
            with c_img:
                try: st.image(logo_filename, width=50) 
                except: st.error("404")
            with c_txt:
                st.markdown(f"#### {title}")
            
            uploaded = st.file_uploader(f"Upload {title}", type=['mp3', 'wav'], key=key, label_visibility="collapsed")
            
            if uploaded:
                with st.spinner("Analisis..."):
                    data = process_audio(uploaded)
                if data and not data.get("error"):
                    st.audio(uploaded)
                    st.metric("SNR Quality", f"{data['snr']:.2f} dB")
                    return {title: data}
                elif data:
                    st.error("Error File")
            else:
                st.info("Menunggu File...", icon="📥")
    return None

res1 = render_upload_clean(col1, "RRI Pro 1", "u1", "pro 1.png")
res2 = render_upload_clean(col2, "RRI Pro 2", "u2", "pro 2.png")
res3 = render_upload_clean(col3, "RRI Pro 4", "u4", "pro 4.png")

if res1: results.update(res1)
if res2: results.update(res2)
if res3: results.update(res3)

# ==========================================
# 5. HASIL & VISUALISASI
# ==========================================
if len(results) > 0:
    st.divider()
    
    # --- 1. KESIMPULAN PEMENANG ---
    best_channel = max(results, key=lambda x: results[x]['snr'])
    best_snr = results[best_channel]['snr']
    
    st.markdown(f"""
    <div class="winner-box">
        <div class="winner-text-head">🏆 HASIL ANALISIS OTOMATIS</div>
        <div class="winner-text-body">
            Sistem merekomendasikan <b>{best_channel}</b> (SNR: <b>{best_snr:.2f} dB</b>).
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 2. TABEL DATA TEKNIS (YANG HILANG TADI) ---
    st.markdown("### 📋 Data Teknis Perbandingan")
    with st.expander("Klik untuk melihat Tabel Angka Detail", expanded=True):
        table_data = []
        for name, data in results.items():
            table_data.append({
                "Nama Channel": name,
                "Kualitas Sinyal (SNR)": f"{data['snr']:.2f} dB",
                "Tingkat Kebisingan (Noise Floor)": f"{data['floor']:.2f} dB"
            })
        st.dataframe(table_data, use_container_width=True)

    # --- 3. GRAFIK VISUALISASI ---
    st.markdown("### 📊 Detail Visualisasi Sinyal (Per Channel)")
    
    g_col1, g_col2, g_col3 = st.columns(3)
    
    def plot_channel_graphs(col, title, data):
        with col:
            with st.container(border=True):
                st.markdown(f"**Analisis {title}**")
                
                ch_color = COLOR_MAP.get(title, "blue")
                plt.style.use('default')

                # OPTIMASI DOWNSAMPLING (Agar Grafik Ringan & Tidak Error)
                DS_WAVE = 100 
                DS_FFT = 10   
                
                # GRAFIK WAVEFORM
                st.caption("1. Waveform (Sinyal vs Noise)")
                fig_wave, ax_wave = plt.subplots(figsize=(5, 2.5))
                ax_wave.plot(data['time'][::DS_WAVE], data['audio'][::DS_WAVE], color='#1E3A8A', alpha=0.4, linewidth=0.5)
                ax_wave.plot(data['time'][::DS_WAVE], data['noise'][::DS_WAVE], color='red', alpha=0.6, linewidth=0.5)
                ax_wave.set_ylabel("Amp")
                ax_wave.set_xticks([]) 
                ax_wave.grid(True, alpha=0.2)
                fig_wave.patch.set_alpha(0.0)
                st.pyplot(fig_wave)

                # GRAFIK SPEKTRUM
                st.caption("2. Spektrum FFT (Frekuensi)")
                fig_fft, ax_fft = plt.subplots(figsize=(5, 2.5))
                ax_fft.plot(data['freqs'][::DS_FFT], data['fft'][::DS_FFT], color=ch_color, alpha=0.9, linewidth=0.8)
                ax_fft.fill_between(data['freqs'][::DS_FFT], data['fft'][::DS_FFT], color=ch_color, alpha=0.3)
                ax_fft.set_xlim(0, 5000)
                ax_fft.set_ylabel("Mag")
                ax_fft.set_xlabel("Hz")
                ax_fft.grid(True, alpha=0.2)
                fig_fft.patch.set_alpha(0.0)
                st.pyplot(fig_fft)

    if "RRI Pro 1" in results: plot_channel_graphs(g_col1, "RRI Pro 1", results["RRI Pro 1"])
    else: g_col1.empty()

    if "RRI Pro 2" in results: plot_channel_graphs(g_col2, "RRI Pro 2", results["RRI Pro 2"])
    else: g_col2.empty()

    if "RRI Pro 4" in results: plot_channel_graphs(g_col3, "RRI Pro 4", results["RRI Pro 4"])
    else: g_col3.empty()

else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Silakan upload file audio untuk melihat visualisasi grafik.")
