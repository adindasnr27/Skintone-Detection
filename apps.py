import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import io
from streamlit_option_menu import option_menu

# ─────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="G2G Shade Finder",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CUSTOM CSS – DESAIN CENTIL & PLAYFUL
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Dancing+Script:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ANIMATIONS */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

@keyframes sparkle {
    0% { opacity: 0.5; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
    100% { opacity: 0.5; transform: scale(0.8); }
}

@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Global */
.stApp {
    background: linear-gradient(135deg, #FFF5F7 0%, #FFE8EE 50%, #FFDDE6 100%);
    background-attachment: fixed;
}

/* Sidebar - Glamour */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #FCE4EC 0%, #F8BBD0 40%, #F48FB1 100%);
    border-right: 3px solid #EC407A;
    box-shadow: 4px 0 30px rgba(233,30,99,0.15);
    padding-top: 20px;
}

[data-testid="stSidebar"]::before {
    content: "✨";
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 2.5rem;
    opacity: 0.5;
    animation: sparkle 2s ease-in-out infinite;
}

[data-testid="stSidebar"]::after {
    content: "💖";
    position: absolute;
    bottom: 80px;
    left: 15px;
    font-size: 2rem;
    opacity: 0.4;
    animation: float 4s ease-in-out infinite;
}

[data-testid="stSidebar"] * {
    color: #4A1A2A !important;
    position: relative;
    z-index: 1;
}

.sidebar-title {
    font-family: 'Dancing Script', cursive !important;
    font-size: 2.2rem !important;
    color: #880E4F !important;
    text-align: center;
    text-shadow: 2px 2px 8px rgba(233,30,99,0.2);
    margin-bottom: 0 !important;
}

.sidebar-subtitle {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: #6A1B3D !important;
    text-align: center;
    opacity: 0.8;
    font-weight: 300 !important;
    letter-spacing: 2px;
}

/* Typography */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #880E4F !important;
}

h1 {
    font-size: 3rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #D81B60, #EC407A, #F06292);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-size: 300% 300%;
    animation: gradient-shift 3s ease-in-out infinite;
    display: inline-block;
}

h1::after {
    content: " ✨";
    -webkit-text-fill-color: initial;
    color: #EC407A;
}

p, li, label, div {
    font-family: 'DM Sans', sans-serif;
    color: #3D1A2B;
}

/* Glam Cards */
.glam-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(233,30,99,0.15);
    border-radius: 20px;
    padding: 25px 30px;
    box-shadow: 0 8px 32px rgba(233,30,99,0.08);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.glam-card::before {
    content: "🌸";
    position: absolute;
    top: -10px;
    right: -5px;
    font-size: 3rem;
    opacity: 0.1;
    transform: rotate(15deg);
}

.glam-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 12px 48px rgba(233,30,99,0.15);
    border-color: #EC407A;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(233,30,99,0.12);
    border-radius: 20px;
    padding: 20px 24px;
    box-shadow: 0 4px 20px rgba(233,30,99,0.06);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(233,30,99,0.12);
}

[data-testid="stMetricValue"] {
    color: #D81B60 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #6A1B3D !important;
    font-weight: 500 !important;
}

/* Buttons - Playful */
.stButton > button {
    background: linear-gradient(135deg, #EC407A, #D81B60, #C2185B);
    background-size: 200% 200%;
    animation: gradient-shift 3s ease-in-out infinite;
    color: white !important;
    border: none;
    border-radius: 50px;
    padding: 12px 32px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(233,30,99,0.25);
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 8px 35px rgba(233,30,99,0.35);
}

.stButton > button:active {
    transform: scale(0.95);
}

/* Uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    border: 3px dashed rgba(233,30,99,0.2);
    border-radius: 20px;
    padding: 30px;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #EC407A;
    background: rgba(255,255,255,0.95);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: rgba(255,255,255,0.5);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 8px;
    border: 1px solid rgba(233,30,99,0.1);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(233,30,99,0.08) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #EC407A, #D81B60) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(233,30,99,0.25);
}

/* Badge - Cute */
.badge-ok {
    display: inline-block;
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    color: #2E7D32;
    border-radius: 50px;
    padding: 5px 16px;
    font-size: 0.82rem;
    font-weight: 600;
    border: 1px solid #A5D6A7;
}

.badge-warn {
    display: inline-block;
    background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
    color: #E65100;
    border-radius: 50px;
    padding: 5px 16px;
    font-size: 0.82rem;
    font-weight: 600;
    border: 1px solid #FFCC80;
}

/* Result Card - Glam */
.glam-result {
    background: linear-gradient(135deg, rgba(252,228,236,0.9), rgba(255,255,255,0.95));
    backdrop-filter: blur(10px);
    border: 2px solid rgba(233,30,99,0.15);
    border-radius: 24px;
    padding: 30px 35px;
    margin-top: 16px;
    box-shadow: 0 8px 40px rgba(233,30,99,0.1);
    position: relative;
    overflow: hidden;
}

.glam-result::before {
    content: "💄";
    position: absolute;
    top: -15px;
    right: -10px;
    font-size: 4rem;
    opacity: 0.08;
    transform: rotate(20deg);
}

.glam-result h2 {
    font-size: 2.5rem !important;
    margin-bottom: 0 !important;
}

.confidence-number {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #D81B60, #EC407A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Recommendation Card */
.rec-card-glam {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    border-left: 5px solid #EC407A;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 14px;
    box-shadow: 0 4px 20px rgba(233,30,99,0.06);
    transition: all 0.3s ease;
}

.rec-card-glam:hover {
    transform: translateX(5px);
    box-shadow: 0 6px 30px rgba(233,30,99,0.12);
}

/* Validation */
.validation-pass {
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    border-left: 5px solid #2E7D32;
    padding: 15px 20px;
    border-radius: 16px;
    margin: 8px 0;
    font-weight: 500;
}

.validation-fail {
    background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
    border-left: 5px solid #E65100;
    padding: 15px 20px;
    border-radius: 16px;
    margin: 8px 0;
    font-weight: 500;
}

/* Camera Container */
.camera-glam {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    border: 3px solid rgba(233,30,99,0.12);
    border-radius: 24px;
    padding: 25px;
    margin-top: 16px;
    box-shadow: 0 4px 20px rgba(233,30,99,0.06);
}

/* Status messages */
.stAlert {
    border-radius: 16px !important;
    border-left: 5px solid !important;
}

/* Image hover */
[data-testid="stImage"] img {
    border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}

[data-testid="stImage"] img:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 40px rgba(0,0,0,0.12);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# KONSTANTA
# ─────────────────────────────────────────
CLASS_NAMES = ["dark", "fair", "light"]
IMG_SIZE    = (224, 224)
MODEL_PATH  = "skin_tone_model.h5"

G2G_RECOMMENDATION = {
    "fair": {
        "shades":   "00 Allegato / 01 Buttercream",
        "skincare": "SPF 50+, Brightening Serum, Vitamin C",
        "tip":      "Kulit fair rentan sunburn – pastikan pakai sunscreen setiap hari!",
    },
    "light": {
        "shades":   "01 Buttercream / 02 Praline",
        "skincare": "SPF 50+, Niacinamide, Hydrating Toner",
        "tip":      "Tone kulit light cocok dengan nuansa nude-pink untuk tampilan natural.",
    },
    "dark": {
        "shades":   "04 Ginger / 05 Cinnamon",
        "skincare": "Moisturizing Cream, SPF 30+, Shea Butter",
        "tip":      "Kulit dark terlihat glowing dengan foundation yang punya undertone warm.",
    },
}

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(pil_img: Image.Image) -> np.ndarray:
    img = pil_img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

def check_image_quality(pil_img: Image.Image):
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    brightness = float(gray.mean())

    if brightness < 80:
        light_status, light_msg = "warn", f"Terlalu gelap (brightness {brightness:.0f})"
    elif brightness > 200:
        light_status, light_msg = "warn", f"Terlalu terang (brightness {brightness:.0f})"
    else:
        light_status, light_msg = "ok", f"Pencahayaan baik (brightness {brightness:.0f})"

    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) > 0:
        face_status, face_msg = "ok", "Wajah terdeteksi"
    else:
        face_status, face_msg = "warn", "Wajah tidak terdeteksi – coba foto lebih dekat"

    return {
        "light_status": light_status, "light_msg": light_msg,
        "face_status": face_status, "face_msg": face_msg,
    }

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "prediction" not in st.session_state:
    st.session_state.prediction = None
    st.session_state.probabilities = None
    st.session_state.uploaded_img = None
    st.session_state.camera_image = None

model = load_model()

# ─────────────────────────────────────────
# SIDEBAR - GLAM VERSION
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">G2G Shade</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-subtitle">✨ find your perfect match ✨</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["🎀 Upload", "🔮 Model Insight", "💖 Beauty Rec"],
        icons=[],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background": "transparent"},
            "icon": {"display": "none"},
            "nav-link": {
                "font-family": "DM Sans, sans-serif",
                "font-weight": "500",
                "font-size": "0.95rem",
                "padding": "12px 18px",
                "border-radius": "12px",
                "margin": "4px 0",
                "transition": "all 0.3s ease",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #EC407A, #D81B60)",
                "color": "white",
                "box-shadow": "0 4px 15px rgba(233,30,99,0.3)",
            },
        }
    )
    
    st.markdown("---")
    st.markdown('<p style="text-align:center;font-size:0.75rem;opacity:0.6;font-weight:300;letter-spacing:1px;">✨ made with love ✨</p>', unsafe_allow_html=True)

# Map selected to page
page_map = {
    "🎀 Upload": "Upload",
    "🔮 Model Insight": "Model Insight",
    "💖 Beauty Rec": "Beauty Recommendation"
}
page = page_map[selected]

# ═══════════════════════════════════════════════════════════════
# PAGE: UPLOAD
# ═══════════════════════════════════════════════════════════════
if page == "Upload":
    st.markdown("# Find Your Perfect Shade")
    st.markdown('<p style="font-size:1.1rem;color:#6A1B3D;margin-top:-10px;">✨ AI-powered skin tone detection, just for you</p>', unsafe_allow_html=True)

    if model is None:
        st.error("🌸 Model belum ditemukan. Pastikan `skin_tone_model.h5` ada di repo.")
        st.stop()

    tab1, tab2 = st.tabs(["📸 Upload Photo", "📷 Take Photo"])

    with tab1:
        st.markdown('<div class="glam-card">', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop your photo here or click to browse", type=["jpg", "jpeg", "png"])
        
        if uploaded:
            pil_img = Image.open(uploaded)
            st.session_state.uploaded_img = pil_img
            st.session_state.camera_image = None
            
            col_img, col_info = st.columns([1, 1], gap="large")

            with col_img:
                st.markdown("#### 💕 Your Photo")
                st.image(pil_img, use_container_width=True)

            with col_info:
                st.markdown("#### ✨ Photo Check")
                quality = check_image_quality(pil_img)
                is_valid = (quality["light_status"] == "ok" and quality["face_status"] == "ok")
                
                if is_valid:
                    st.markdown(f"""
                    <div class="validation-pass">
                        💖 {quality["light_msg"]}<br>
                        💖 {quality["face_msg"]}<br>
                        <span style="color:#2E7D32;font-weight:600;">✨ Perfect! Let's analyze your skin ✨</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="validation-fail">
                        🌸 {quality["light_msg"] if quality["light_status"] == "warn" else quality["face_msg"] if quality["face_status"] == "warn" else ""}
                        <br><br>
                        <strong>💡 Quick Tips:</strong><br>
                        • Find better lighting ✨<br>
                        • Position your face clearly 💖
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                if is_valid:
                    st.markdown("#### 💄 Analyzing Your Skin")
                    with st.spinner("🌸 Computing your perfect shade..."):
                        tensor = preprocess_image(pil_img)
                        probs = model.predict(tensor, verbose=0)[0]
                        idx = int(np.argmax(probs))
                        label = CLASS_NAMES[idx]
                        conf = float(probs[idx]) * 100

                    st.session_state.prediction = label
                    st.session_state.probabilities = probs

                    st.markdown(f"""
                    <div class="glam-result">
                        <h2>✨ {label.title()}</h2>
                        <p style="font-size:0.95rem;color:#6A1B3D;">Your detected skin tone</p>
                        <hr style="border-color:rgba(233,30,99,0.15);margin:12px 0;">
                        <p class="confidence-number">{conf:.1f}%</p>
                        <p style="font-size:0.85rem;color:#6A1B3D;">Confidence Score</p>
                        <br>
                        <span style="font-size:0.9rem;color:#6A1B3D;">💖 Check <strong>Beauty Rec</strong> for your G2G shade!</span>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="camera-glam">', unsafe_allow_html=True)
        st.markdown("#### 📷 Capture Your Glow")
        st.caption("✨ Make sure you're in good lighting and your face is clearly visible")
        
        camera_image = st.camera_input("📸 Smile!", label_visibility="collapsed")
        
        if camera_image is not None:
            pil_img = Image.open(camera_image)
            st.session_state.camera_image = pil_img
            st.session_state.uploaded_img = pil_img
            
            col_cam, col_cam_info = st.columns([1, 1], gap="large")

            with col_cam:
                st.markdown("#### 💕 Your Photo")
                st.image(pil_img, use_container_width=True)

            with col_cam_info:
                st.markdown("#### ✨ Quality Check")
                quality = check_image_quality(pil_img)
                is_valid = (quality["light_status"] == "ok" and quality["face_status"] == "ok")
                
                if is_valid:
                    st.markdown(f"""
                    <div class="validation-pass">
                        💖 {quality["light_msg"]}<br>
                        💖 {quality["face_msg"]}<br>
                        <span style="color:#2E7D32;font-weight:600;">🎉 Perfect shot! Analyzing now...</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("#### 💄 Your Result")
                    with st.spinner("🌸 Computing your perfect shade..."):
                        tensor = preprocess_image(pil_img)
                        probs = model.predict(tensor, verbose=0)[0]
                        idx = int(np.argmax(probs))
                        label = CLASS_NAMES[idx]
                        conf = float(probs[idx]) * 100

                    st.session_state.prediction = label
                    st.session_state.probabilities = probs

                    st.markdown(f"""
                    <div class="glam-result">
                        <h2>✨ {label.title()}</h2>
                        <p style="font-size:0.95rem;color:#6A1B3D;">Your detected skin tone</p>
                        <hr style="border-color:rgba(233,30,99,0.15);margin:12px 0;">
                        <p class="confidence-number">{conf:.1f}%</p>
                        <p style="font-size:0.85rem;color:#6A1B3D;">Confidence Score</p>
                        <br>
                        <span style="font-size:0.9rem;color:#6A1B3D;">💖 Check <strong>Beauty Rec</strong> for your G2G shade!</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="validation-fail">
                        🌸 Oops! Let's try again<br><br>
                        {quality["light_msg"] if quality["light_status"] == "warn" else ""}
                        {quality["face_msg"] if quality["face_status"] == "warn" else ""}
                        <br><br>
                        <strong>💡 Quick Tips:</strong><br>
                        • Find better lighting ✨<br>
                        • Center your face in the frame 💖<br>
                        • Avoid shadows on your face 🌸
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🌸 Click the camera button above to take your photo!")
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: MODEL INSIGHT
# ═══════════════════════════════════════════════════════════════
elif page == "Model Insight":
    st.markdown("# 🔮 Model Insight")
    st.markdown('<p style="font-size:1.1rem;color:#6A1B3D;margin-top:-10px;">✨ Peek into how AI sees your skin tone</p>', unsafe_allow_html=True)

    if st.session_state.probabilities is None:
        st.warning("🌸 Upload a photo first on the **Upload** page!")
        st.stop()

    probs = st.session_state.probabilities
    pred = st.session_state.prediction
    conf = float(probs[CLASS_NAMES.index(pred)]) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Confidence", f"{conf:.1f}%", help="How confident the AI is")
    col2.metric("🏷️ Detected", pred.title(), help="Your skin tone category")
    col3.metric("📊 Classes", len(CLASS_NAMES), help="Total skin tone categories")

    st.markdown("---")
    st.markdown("#### 📊 Probability Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["#EC407A" if c == pred else "#F48FB1" for c in CLASS_NAMES]
    bars = ax.barh(
        [c.title() for c in CLASS_NAMES],
        [p * 100 for p in probs],
        color=colors, height=0.5, edgecolor="white", linewidth=2,
    )
    for bar, p in zip(bars, probs):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{p*100:.1f}%", va="center", fontsize=12, fontweight="bold", color="#3D1A2B")
    ax.set_xlim(0, 110)
    ax.set_xlabel("Probability (%)", fontsize=11, fontweight="500")
    ax.set_facecolor("rgba(255,255,255,0.3)")
    fig.patch.set_facecolor("transparent")
    ax.spines[["top","right"]].set_visible(False)
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.markdown("#### 📋 Detailed Breakdown")
    import pandas as pd
    rows = []
    for cls, p in zip(CLASS_NAMES, probs):
        rows.append({
            "Skin Tone": f"🌸 {cls.title()}",
            "Probability": f"{p*100:.1f}%",
            "Status": "🎯 Predicted" if cls == pred else ""
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: BEAUTY RECOMMENDATION
# ═══════════════════════════════════════════════════════════════
elif page == "Beauty Recommendation":
    st.markdown("# 💖 Beauty Recommendation")
    st.markdown('<p style="font-size:1.1rem;color:#6A1B3D;margin-top:-10px;">✨ Your personalized G2G beauty guide</p>', unsafe_allow_html=True)

    if st.session_state.prediction is None:
        st.warning("🌸 Upload a photo first on the **Upload** page!")
        st.stop()

    pred = st.session_state.prediction
    rec = G2G_RECOMMENDATION[pred]
    img = st.session_state.uploaded_img

    col_photo, col_rec = st.columns([1, 1.4], gap="large")

    with col_photo:
        if img:
            st.markdown("#### 💕 Your Photo")
            st.image(img, use_container_width=True)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(252,228,236,0.3),rgba(255,255,255,0.5));border-radius:16px;padding:15px 20px;text-align:center;border:1px solid rgba(233,30,99,0.1);">
            <span style="font-size:2rem;">🌸</span>
            <p style="font-weight:600;color:#6A1B3D;margin:0;">Skin Tone: <span style="color:#D81B60;">{pred.title()}</span></p>
        </div>
        """, unsafe_allow_html=True)

    with col_rec:
        st.markdown(f"### 💖 Your Perfect Match")
        
        st.markdown(f"""
        <div class="rec-card-glam">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <span style="font-size:1.2rem;">💄</span>
                <span style="font-size:0.78rem;text-transform:uppercase;letter-spacing:1px;color:#6A1B3D;font-weight:600;">G2G Foundation Shade</span>
            </div>
            <p style="font-size:1.3rem;font-weight:700;color:#D81B60;margin:0;">{rec['shades']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rec-card-glam">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <span style="font-size:1.2rem;">🧴</span>
                <span style="font-size:0.78rem;text-transform:uppercase;letter-spacing:1px;color:#6A1B3D;font-weight:600;">Skincare Recommendation</span>
            </div>
            <p style="font-size:1.05rem;font-weight:500;color:#3D1A2B;margin:0;">{rec['skincare']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rec-card-glam" style="border-left-color:#F48FB1;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <span style="font-size:1.2rem;">💡</span>
                <span style="font-size:0.78rem;text-transform:uppercase;letter-spacing:1px;color:#6A1B3D;font-weight:600;">Beauty Tip</span>
            </div>
            <p style="font-size:0.95rem;color:#3D1A2B;margin:0;">{rec['tip']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.caption("💖 Rekomendasi berdasarkan prediksi AI. Lakukan swatching sebelum membeli.")

    # G2G Shade Reference
    st.markdown("---")
    st.markdown("#### 🎨 All G2G Shades")
    shades = [
        ("00", "Allegato", "#F5D5B0"),
        ("01", "Buttercream", "#F2C89A"),
        ("02", "Praline", "#D4A278"),
        ("03", "Cookies", "#C49060"),
        ("04", "Ginger", "#B07848"),
        ("05", "Cinnamon", "#8B5E3C"),
    ]
    cols = st.columns(6)
    for col, (code, name, color) in zip(cols, shades):
        with col:
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="width:60px;height:60px;border-radius:50%;background:{color};
                            margin:0 auto 8px;border:3px solid rgba(233,30,99,0.2);
                            box-shadow:0 4px 20px rgba(0,0,0,0.08);
                            transition:all 0.3s ease;">
                </div>
                <p style="font-size:0.7rem;font-weight:700;color:#D81B60;margin:0;">{code}</p>
                <p style="font-size:0.72rem;color:#6A1B3D;margin:0;">{name}</p>
            </div>
            """, unsafe_allow_html=True)
