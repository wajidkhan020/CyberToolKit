import streamlit as st
import hashlib
import requests


def main():
    st.set_page_config(
        page_title="Breach Scanner",
        layout="wide"
    )


st.markdown("""
<style>
    .stApp {
    background-color: #0a0e27 !important;
    color: #00ffff;
}
    section[data-testid="stSidebar"] {
        background-color: #05071a !important;
        border-right: 2px solid rgba(0, 255, 255, 0.2) !important;
    }
  /* Sidebar styling - Fixed, non-collapsible, scrollable */
       section[data-testid="stSidebar"] {
        background-color: #05071a !important;
        border-right: 2px solid rgba(0, 255, 255, 0.2) !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        flex-shrink: 0 !important;
        flex-grow: 0 !important;
    }
    /* Make sidebar scrollable */
    section[data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        padding: 2rem 1rem !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        max-height: 100vh !important;
    }
    
    /* Custom scrollbar for sidebar */
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
        width: 8px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 10px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {
        background: rgba(0,255,255,0.5) !important;
        border-radius: 10px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {
        background: rgba(0,255,255,0.8) !important;
    }
    
    /* Prevent sidebar from collapsing */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
    }
    
    section[data-testid="stSidebar"][aria-expanded="true"] {
        margin-left: 0 !important;
    }
    
    /* Hide collapse button */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }
    
    /* Main content scrolling */
    .main .block-container {
        overflow-y: auto !important;
        max-height: 100vh !important;
    }
    
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }
       
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;} */
    
    .block-container {
        padding-top: 1rem !important;
    }
    
    h1 {
        color: #00ffff;
        text-align: center;
        font-size: 3rem;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.8),
                     0 0 40px rgba(0, 255, 255, 0.5),
                     0 0 60px rgba(0, 255, 255, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
        margin-bottom: 0.5rem;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 255, 255, 0.8); }
        to { text-shadow: 0 0 30px rgba(0, 255, 255, 1), 0 0 60px rgba(0, 255, 255, 0.7); }
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(0, 20, 40, 0.8) !important;
        color: #00ffff !important;
        border: 2px solid rgba(0, 255, 255, 0.4) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
        box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.1) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5) !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00d9ff 0%, #0066ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 40px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.5),
                    0 5px 15px rgba(0, 102, 255, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.8),
                    0 8px 20px rgba(0, 102, 255, 0.6) !important;
    }
    
    .success-box {
        background: rgba(0, 255, 100, 0.1);
        border: 2px solid #00ff64;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        color: #00ff64;
        box-shadow: 0 0 20px rgba(0, 255, 100, 0.3);
    }
    
    .danger-box {
        background: rgba(255, 0, 100, 0.1);
        border: 2px solid #ff0064;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        color: #ff0064;
        box-shadow: 0 0 20px rgba(255, 0, 100, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 100, 0.3); }
        50% { box-shadow: 0 0 30px rgba(255, 0, 100, 0.6); }
    }
    
    .warning-box {
        background: rgba(255, 200, 0, 0.1);
        border: 2px solid #ffc800;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        color: #ffc800;
        box-shadow: 0 0 20px rgba(255, 200, 0, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: rgba(0, 255, 255, 0.6);
        font-size: 0.9rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    
    .status-indicators {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: rgba(0, 255, 255, 0.6);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00ff64;
        box-shadow: 0 0 10px #00ff64;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    .info-footer {
        text-align: center;
        color: rgba(0, 255, 255, 0.4);
        font-size: 0.75rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(0, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1> BREACH SCANNER</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"> Real-Time Breach Detection & Security Analysis </p>', unsafe_allow_html=True)


st.markdown('<div class="glass-container">', unsafe_allow_html=True)


def check_password_leak(password):
    try:
        
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        
        
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        
        if response.status_code != 200:
            return "error", " Error contacting breach database❌"
        
        
        for line in response.text.splitlines():
            hash_suffix, count = line.split(':')
            if hash_suffix == suffix:
                return "danger", f" BREACH DETECTED\n\nPassword found {int(count):,} times in data breaches!⚠️"
        
        return "success", "✅ SECURE\n\nPassword not found in known breaches"
    
    except Exception as e:
        return "error", f" Weak Internet ya phir Internet hi nahi beta: "


password = st.text_input("🔒 ENTER PASSWORD", type="password", placeholder="••••••••••••")
with st.sidebar:
    if st.button("⬅ Back"):
        st.session_state.current_module = None
        st.rerun()   # force instant refresh
    st.header("ℹ️ About")
    st.markdown("""
    <h3 style='color: white; font-size: 1 rem; font-weight: bold; margin-top: 1 rem;'> Breach Scanner Help you:</h3>
    
   * **<span style='color: white; font-weight: bold;'>Real-Time</span> Leak Check:** Compares your password against billions of compromised accounts.
    * **<span style='color: white; font-weight: bold;'>Security</span> Validation:** Instantly identifies if your credential is known to hackers.
    * **<span style='color: white; font-weight: bold;'>Privacy-First:</span>** Uses advanced hashing to ensure your actual password is never exposed.
    * **<span style='color: white; font-weight: bold;'>Breach</span> Notification:** Provides clear warnings if a vulnerability is detected.
    
    <h3 style='color: white; font-size: 1.3rem; font-weight: bold; margin-top: 1 rem;'> How It Works:</h3>
    
    * **<span style='color: white; font-weight: bold;'>Hashing:</span>** Your password is first converted into a **SHA-1 hash**.
    * **<span style='color: white; font-weight: bold;'>K-Anonymity:</span>** Only first 5 hash characters are sent.
    * **<span style='color: white; font-weight: bold;'>Local Comparison:</span>** Remaining hash is matched locally.
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🔒 This tool only scans publicly broadcast information. It does NOT hack or attack networks.")


    
if st.button(" Scan Now"):
    if not password:
        st.markdown('<div class="warning-box"> Please enter a password to check ⚠️</div>', unsafe_allow_html=True)
    else:
        with st.spinner('🔄 Scanning database...'):
            result_type, result_message = check_password_leak(password)
            
            if result_type == "success":
                st.markdown(f'<div class="success-box">{result_message}</div>', unsafe_allow_html=True)
            elif result_type == "danger":
                st.markdown(f'<div class="danger-box">{result_message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-box">{result_message}</div>', unsafe_allow_html=True)


st.markdown('''
<div class="info-footer">
    Secure • Private • Anonymous
</div>
''', unsafe_allow_html=True)


st.markdown('''
<div class="status-indicators">
    <div class="status-item">
        <div class="status-dot"></div>
        <span>System Online</span>
    </div>
    <div class="status-item">
        <div class="status-dot" style="animation-delay: 0.5s;"></div>
        <span>Database Active</span>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)