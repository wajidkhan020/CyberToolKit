import streamlit as st
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="CyberNova Suit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def set_bg(image_file):
    try:
        with open(image_file, 'rb') as f:  # <-- use the image file
            encoded = base64.b64encode(f.read()).decode()
        
        page_bg = f"""
        <style>
        .stApp {{
            position: relative;
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 0;
        }}
        .stApp > div {{
            position: relative;
            z-index: 1;
        }}
       
        /* Header */
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        
        
        h1 {{
            font-weight: 700;
            color: #00ffff !important;
            text-shadow: 0 0 30px rgba(0,255,255,1), 2px 2px 8px rgba(0,0,0,1);
            background: linear-gradient(135deg, rgba(0,20,40,0.95), rgba(20,0,60,0.95)) !important;
            padding: 25px 40px !important;
            border-radius: 15px !important;
            border: 3px solid rgba(0,255,255,0.6) !important;
            box-shadow: 0 0 40px rgba(0,255,255,0.4);
            font-size: 2.5rem !important;
            text-align: center !important;
            margin-bottom: 30px !important;
        }}
        
        h2, h3, h4, p, li, span, div {{
            color: #ffffff !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
        }}
        
       
        .module-card {{
            background: linear-gradient(135deg, rgba(0,20,40,0.9), rgba(20,0,60,0.9)) !important;
            padding: 30px !important;
            border-radius: 15px !important;
            border: 2px solid rgba(0,255,255,0.4) !important;
            box-shadow: 0 0 30px rgba(0,255,255,0.3) !important;
            transition: all 0.3s ease !important;
            margin-bottom: 20px !important;
            cursor: pointer !important;
        }}
        
        .module-card:hover {{
            transform: translateY(-5px) !important;
            border-color: rgba(0,255,255,0.8) !important;
            box-shadow: 0 0 50px rgba(0,255,255,0.6) !important;
        }}
        
       
        .stButton > button {{
            background: linear-gradient(135deg, #0a4d68, #1a7d9c) !important;
            color: #00ffff !important;
            border: 2px solid rgba(0,255,255,0.5) !important;
            border-radius: 12px !important;
            box-shadow: 0 0 20px rgba(0,255,255,0.4) !important;
            font-weight: 700 !important;
            font-size: 1.2rem !important;
            padding: 15px 30px !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 0 35px rgba(0,255,255,0.8) !important;
            background: linear-gradient(135deg, #1a6d8c, #2a8dac) !important;
            transform: translateY(-3px) !important;
        }}
        
     
        .stAlert {{
            background: linear-gradient(135deg, rgba(0,20,40,0.8), rgba(0,40,80,0.8)) !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 20px rgba(0,255,255,0.2) !important;
        }}
        
        hr {{
            border-color: rgba(0,255,255,0.3) !important;
            box-shadow: 0 0 10px rgba(0,255,255,0.2) !important;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    except:
        pass


set_bg("main.png")


MODULES = {
    "Phishing Email Detection": {
        "file": "phishing_detector.py",
        "description": "AI-powered phishing email detection using LSTM neural networks. Analyzes email content, identifies suspicious patterns, and verifies sender domains.",
        "icon": "",
        "color": "#ff416c"
    },
    "Password Strength Checker": {
        "file": "password_checker.py",
        "description": "Advanced password analysis with entropy calculation, breach database checking, pattern detection, and crack time estimation.",
        "icon": "",
        "color": "#667eea"
    },
    "Breach Scanner": {
        "file": "breach_scanner.py",
        "description": "Check if your passwords have been compromised in data breaches using the Have I Been Pwned API with k-anonymity protection.",
        "icon": "",
        "color": "#f7971e"
    },
    "Advance URL Analyzer": {
        "file": "wifi_analyzer.py",
        "description": "Scan and analyze URLs in real time, detect suspicious domains, identify phishing patterns, check for hidden redirects, and provide security risk assessment with safety recommendations.",
        "icon": "",
        "color": "#11998e"
    }
}

def run_module(module_file):
    """Execute the selected module"""
    module_path = f"modules/{module_file}"  # <-- point to modules folder
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, globals())
    except FileNotFoundError:
        st.error(f"Module file not found: {module_path}")
    except Exception as e:
        st.error(f"Error running module: {str(e)}")

def show_home():
    """Display the home page"""
    
    # title
    st.markdown("""
        <h1>CyberNova Guard</h1>
    """, unsafe_allow_html=True)
    

    st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(0,20,40,0.8), rgba(20,0,60,0.8)); 
        border-radius: 15px; border: 2px solid rgba(0,255,255,0.3); margin-bottom: 30px;'>
            <h2 style='color: #00ffff; margin: 0;'>🔒 Cybersecurity Toolkit</h2>
            <p style='font-size: 1.2rem; margin: 10px 0; color: #ffffff;'>
                Protect your digital life
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    modules_list = list(MODULES.items())
    
    with col1:
        for i in [0, 2]:
            if i < len(modules_list):
                module_name, module_info = modules_list[i]
                
                st.markdown(f"""
                    <div class="module-card">
                        <h2 style='color: #00ffff; margin-bottom: 15px;'>{module_info['icon']} {module_name}</h2>
                        <p style='font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;'>{module_info['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f" Launch {module_name}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.current_module = module_name
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    with col2:
        for i in [1, 3]:
            if i < len(modules_list):
                module_name, module_info = modules_list[i]
                
                st.markdown(f"""
                    <div class="module-card">
                        <h2 style='color: #00ffff; margin-bottom: 15px;'>{module_info['icon']} {module_name}</h2>
                        <p style='font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;'>{module_info['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f" Launch {module_name}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.current_module = module_name
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # FOOTER INFO 
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #00ffff; font-size: 1.1rem;'>
            <p> <strong>Soon:</strong> we will be adding more security analysis tool</p>
            <p style='font-size: 0.9rem; color: rgba(0,255,255,0.7);'>Built with ❤️ for Gc University | Protecting Digital Lives</p>
        </div>
    """, unsafe_allow_html=True)

def main():

    if 'current_module' not in st.session_state:
        st.session_state.current_module = None
    
 #sidebar
    if st.session_state.current_module is None:
        # Show home dashboard
        show_home()
    else:
    # Directly load selected module (no Home button)
        module_info = MODULES[st.session_state.current_module]
        run_module(module_info["file"])

    
if __name__ == "__main__":
    main()