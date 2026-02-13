import streamlit as st
import joblib
import numpy as np
import cv2  # We will use OpenCV instead of pyzbar
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="QR Shield AI", page_icon="🛡️", layout="centered")

# --- LOAD THE BRAIN ---
@st.cache_resource
def load_ai_model():
    try:
        # Load the model from file
        return joblib.load('qr_fraud_model.pkl')
    except FileNotFoundError:
        return None


# --- TRUSTED DOMAINS (Whitelist) ---
WHITELIST = [
    "google.com", "www.google.com", 
    "youtube.com", "www.youtube.com",
    "facebook.com", "instagram.com",
    "wikipedia.org", "amazon.com"
]

def is_whitelisted(url):
    # 1. Check for UPI Payment Links (Always Safe for this demo)
    if url.lower().startswith("upi://"):
        return True
    
    # 2. Check for Whitelisted Domains
    for domain in WHITELIST:
        if domain in url.lower():
            return True
            
    return False

model = load_ai_model()

# --- FEATURE EXTRACTION HELPER ---
def extract_features(url):
    features = [
        len(url), url.count('.'), url.count('-'), url.count('@'),
        url.count('?'), 1 if "https" in url else 0,
        sum(c.isdigit() for c in url),
        1 if ".xyz" in url or ".top" in url else 0
    ]
    return np.array(features).reshape(1, -1)

# --- UI HEADER ---
st.title("🛡️ QR Shield AI")
st.markdown("### Hybrid AI Security for QR Code Detection")
st.info("This system uses Machine Learning to detect phishing patterns in QR codes.")

# --- CHECK IF MODEL IS LOADED ---
if model is None:
    st.error("❌ Error: 'qr_fraud_model.pkl' not found. Please move the model file into this folder!")
else:
    # --- TABS FOR INPUT ---
    tab1, tab2 = st.tabs(["🖼️ Upload QR Image", "🔗 Paste URL Manually"])

    # TAB 1: IMAGE SCANNER
    with tab1:
        uploaded_file = st.file_uploader("Upload a QR Code (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption='Scanned Image', width=200)
            
            # --- NEW DECODING LOGIC (OpenCV) ---
            try:
                # Convert PIL image to OpenCV format (numpy array)
                img_array = np.array(image.convert('RGB'))
                # OpenCV uses BGR, PIL uses RGB, convert it
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                
                # Initialize OpenCV QR Detector
                detector = cv2.QRCodeDetector()
                url, bbox, straight_qrcode = detector.detectAndDecode(img_array)
                
                if url:
                    st.write(f"**Decoded Link:** `{url}`")
                    
                    # AI Prediction
                    if is_whitelisted(url):
                        probability = 0.0
                    else:
                        features = extract_features(url)
                        probability = model.predict_proba(features)[0][1]
                    
                    st.divider()
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Risk Score", f"{probability*100:.1f}%")
                    
                    with col2:
                        if probability > 0.5:
                            st.error("🚨 MALICIOUS")
                        else:
                            st.success("✅ SAFE")
                            
                else:
                    st.warning("⚠️ No QR code detected. Try a clearer picture or crop closer to the QR.")
            except Exception as e:
                st.error(f"Error processing image: {e}")

    # TAB 2: MANUAL URL CHECK
    with tab2:
        user_url = st.text_input("Paste a URL to check:")
        
        if st.button("Analyze Link"):
            if user_url:
                if is_whitelisted(user_url):
                    prob = 0.0
                else:
                    features = extract_features(user_url)
                    prob = model.predict_proba(features)[0][1]
                
                if prob > 0.5:
                    st.error(f"🚨 **DANGER DETECTED** (Confidence: {prob*100:.1f}%)")
                    st.markdown("This link contains patterns commonly found in **Phishing Attacks**.")
                else:
                    st.success(f"✅ **SAFE** (Confidence: {(1-prob)*100:.1f}%)")
                    st.markdown("This link looks legitimate.")