import streamlit as st
import tensorflow as tf
import pickle
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
import base64
import os

st.set_page_config(
    page_title="Phishing Email Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)


TRUSTED_DOMAINS = [
    'google.com', 'gmail.com', 'microsoft.com', 'outlook.com', 
    'apple.com', 'amazon.com', 'facebook.com', 'linkedin.com',
    'twitter.com', 'instagram.com', 'yahoo.com', 'github.com'
]

# Custom CSS UI background image
def set_custom_style(image_file="phish.jpg"):

    bg_image = "phish.jpg"
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            bg_image = f'background-image: url("data:image/jpg;base64,{encoded}");'
    except:
        
        bg_image = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"
    st.markdown("""
    <style>
        
        .stApp {{
           background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        
        h1 {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            padding: 20px;
            background: linear-gradient(135deg, rgba(0,0,0,0.3), rgba(0,0,0,0.2));
            border-radius: 15px;
            border: 2px solid rgba(255,255,255,0.2);
            text-align: center;
            margin-bottom: 20px;
        }
        
        
        h2, h3 {
            color: #ffffff !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        }
        
        
        p, div, span, label {
            color: #ffffff !important;
        }
        
    
        .stTextArea textarea {
        background: rgba(10, 25, 47, 0.95) !important;  /* NAVY BLUE */
        color: #ffffff !important;  /* WHITE TEXT */
        border: 2px solid rgba(0,255,255,0.4) !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }
            
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #76ba2) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(0,0,0,0.4), rgba(0,0,0,0.6)) !important;
            border-right: 2px solid rgba(255,255,255,0.2) !important;
            width: 21rem !important;               /* Add this */
            min-width: 21rem !important;           /* Add this */
            max-width: 21rem !important;           /* Add this */
            flex-shrink: 0 !important;             /* Add this */
            flex-grow: 0 !important;               /* Add this */
            resize: none !important;  
        }
                
        /* Hide resize handle */
        section[data-testid="stSidebar"]::after {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        /* Hide collapse button */
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        
        [data-testid="stSidebarHeader"] {
            display: none !important;
        }
        /* Sidebar scrolling */
    section[data-testid="stSidebar"] > div:first-child {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        max-height: 100vh !important;
        padding: 2rem 1rem !important;
    }
    
    /* Custom scrollbar */
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
        width: 8px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 10px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.5) !important;
    }
        
        button[kind="header"] {
            display: none !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #ffffff !important;
            font-size: 1rem !important;
        }
        
        
        .stAlert {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
        }
        
        
        code {
            background: rgba(0, 0, 0, 0.3) !important;
            color: #00ff00 !important;
            padding: 10px !important;
            border-radius: 5px !important;
        }
        
        
        .stSpinner > div {
            border-top-color: #ffffff !important;
        }
        
        hr {
            border-color: rgba(255, 255, 255, 0.3) !important;
            margin: 20px 0 !important;
        }
        
        
        .result-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            margin: 15px 0;
            border: 2px solid rgba(255,255,255,0.3);
        }
        
        
        .risk-high {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(255,65,108,0.4);
        }
        
        .risk-medium {
            background: linear-gradient(135deg, #f7971e, #ffd200);
            color: #333;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(247,151,30,0.4);
        }
        
        .risk-low {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(17,153,142,0.4);
        }
        
        
        .flag-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 8px;
            border-left: 4px solid #ff4b2b;
        }
    </style>
    """, unsafe_allow_html=True)

# Load model and tokenizer (cached for performance)
@st.cache_resource
def load_model_and_tokenizer():
    """Load trained model and tokenizer"""
    try:
        model_path = os.path.join( "phishing_detector.keras")
        model = keras.models.load_model(model_path)
        
        with open('tokenizer.pkl', 'rb') as f:
            tokenizer = pickle.load(f)
        
        with open('config.pkl', 'rb') as f:
            config = pickle.load(f)
        
        return model, tokenizer, config
    except Exception as e:
        st.error(f" Error loading model files: {e}")
        return None, None, None

# Text cleaning function
def clean_email_text(text):
    """Clean email text"""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\.\S+', 'URL', text)
    text = re.sub(r'\S+@\S+', 'EMAIL', text)
    text = re.sub(r'\d+', 'NUM', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Prediction function with domain checking
def predict_phishing(email_text, model, tokenizer, config):
    """Predict if email is phishing with domain checking"""
    
    # Extract domains from email
    domain_pattern = r'(?:@|://|www\.)\s*([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    domains = re.findall(domain_pattern, email_text.lower())
    domains = [d.strip().lstrip('.') for d in domains]
    domains = list(dict.fromkeys(domains))
    
    # Check if any domain is trusted
    is_trusted = False
    trusted_domain = None
    trusted_match_reason = None
    
    for domain in domains:
        for trusted in TRUSTED_DOMAINS:
            if domain == trusted or domain.endswith('.' + trusted):
                is_trusted = True
                trusted_domain = trusted
                trusted_match_reason = "exact_or_subdomain"
                break
        if is_trusted:
            break
    
    # Clean text
    clean_text = clean_email_text(email_text)
    
    # Convert to sequence
    seq = tokenizer.texts_to_sequences([clean_text])
    padded = pad_sequences(seq, maxlen=config['MAX_LENGTH'], padding='post')
    
    # Get AI prediction
    prediction = model.predict(padded, verbose=0)[0][0]
    ai_score = float(prediction * 100)
    
    # Adjust score if trusted domain
    if is_trusted:
        risk_score = ai_score * 0.3
    else:
        risk_score = ai_score
    
    debug = {
        'extracted_domains': domains,
        'is_trusted': is_trusted,
        'trusted_domain': trusted_domain,
        'trusted_match_reason': trusted_match_reason,
        'ai_score': ai_score,
        'adjusted_risk': risk_score
    }
    
    return risk_score, clean_text, debug

# Main app
def main():
    # Apply custom styling
    set_custom_style()
    
    # Load model
    model, tokenizer, config = load_model_and_tokenizer()
    
    if model is None:
        st.error(" Failed to load model. Please ensure model files exist.")
        return
    
    # Header
    st.title(" Phishing Email Detector")
    
    # Info banner
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric(" Model Accuracy", f"{config['test_accuracy']*100:.2f}%")
    with col_info2:
        st.metric(" Vocabulary", f"{config['MAX_WORDS']:,}")
    with col_info3:
        st.metric(" Technology", "LSTM Neural Network")
    
    st.markdown("---")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📧 Email Analysis", "📊 Statistics", "ℹ️ About"])
    
    with tab1:
        # Create two columns
        col1, col2 = st.columns([3, 2], gap="large")
        
        with col1:
            st.subheader("📧 Enter Email Content")
            
            # Text input
            email_input = st.text_area(
                "Paste suspicious email here:",
                height=300,
                placeholder="Example: URGENT! Your account has been suspended. Click here to verify...",
                key="email_input"
            )
            
            # Analyze button
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_btn = st.button(" Analyze Email", type="primary", use_container_width=True)
            
            # Sample emails section
            st.markdown("---")
            st.markdown("### 📝 Quick Test Samples")
            
            col_test1, col_test2 = st.columns(2)
            
            with col_test1:
                if st.button("Test Phishing Email", use_container_width=True):
                    st.session_state.email_input = """URGENT SECURITY ALERT!
Your account has been temporarily suspended due to suspicious activity detected.
Click here immediately to verify your identity: http://fake-bank-security.com/verify
You have 24 hours to respond or your account will be permanently closed.
Action required: Confirm your personal details and payment information.
Failure to comply will result in account termination!"""
                    st.rerun()
            
            with col_test2:
                if st.button(" Test Safe Email", use_container_width=True):
                    st.session_state.email_input = """Hi Team,
Hope you're doing well! Just wanted to share the weekly project update with everyone.
The development phase is progressing smoothly and we're on track to meet our deadline.
Please find the attached progress report for your review.
Let me know if you have any questions or need clarification on any points.
Best regards,
John Smith
Project Manager"""
                    st.rerun()
        
        with col2:
            st.subheader(" Analysis Results")
            
            if analyze_btn and email_input:
                with st.spinner(" AI is analyzing your email..."):
                    # Predict
                    risk_score, clean_text, debug = predict_phishing(email_input, model, tokenizer, config)
                    
                    # Determine risk level
                    if risk_score > 70:
                        risk_level = "HIGH RISK"
                        risk_class = "risk-high"
                        risk_emoji = "🔴"
                        result_msg = "⚠️ This email is likely PHISHING!"
                        recommendation = "DO NOT click any links or provide personal information!"
                    elif risk_score > 40:
                        risk_level = "MEDIUM RISK"
                        risk_class = "risk-medium"
                        risk_emoji = "🟡"
                        result_msg = "⚠️ Be cautious with this email"
                        recommendation = "Verify sender before taking any action."
                    else:
                        risk_level = "LOW RISK"
                        risk_class = "risk-low"
                        risk_emoji = "🟢"
                        result_msg = "✅ This email appears safe"
                        recommendation = "Email looks legitimate, but stay vigilant."
                    
                    # Display results card
                    st.markdown(f"""
                    <div class="{risk_class}">
                        <h2 style="margin: 0;">{risk_emoji} {risk_level}</h2>
                        <h1 style="margin: 15px 0; font-size: 3rem;">{risk_score:.1f}%</h1>
                        <p style="font-size: 1.2rem; margin: 10px 0;">{result_msg}</p>
                        <p style="font-size: 1rem; margin: 5px 0; opacity: 0.9;">{recommendation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Domain trust info
                    if debug['is_trusted']:
                        st.success(f" **Trusted Domain Detected:** {debug['trusted_domain']}")
                        st.caption("Risk score reduced by 70% due to trusted sender domain")
                    
                    # Detailed analysis
                    st.markdown("###  Detailed Analysis")
                    
                    # Check for red flags
                    red_flags = []
                    email_lower = email_input.lower()
                    
                    urgent_words = ['urgent', 'immediately', 'act now', 'suspended', 'verify', 'confirm', 'required']
                    money_words = ['won', 'prize', 'claim', 'million', 'dollars', 'winner', 'lottery', 'inheritance']
                    threat_words = ['suspended', 'closed', 'terminated', 'blocked', 'limited', 'expire', 'failure']
                    personal_words = ['password', 'credit card', 'ssn', 'social security', 'bank account', 'pin']
                    
                    for word in urgent_words:
                        if word in email_lower:
                            red_flags.append(f" Urgent language: '{word}'")
                    
                    for word in money_words:
                        if word in email_lower:
                            red_flags.append(f" Money-related: '{word}'")
                    
                    for word in threat_words:
                        if word in email_lower:
                            red_flags.append(f" Threatening: '{word}'")
                    
                    for word in personal_words:
                        if word in email_lower:
                            red_flags.append(f" Requests personal info: '{word}'")
                    
                    if 'http://' in email_input or 'www.' in email_input:
                        red_flags.append("🔗 Contains links (verify before clicking)")
                    
                    if debug['extracted_domains']:
                        red_flags.append(f" Domains found: {', '.join(debug['extracted_domains'][:3])}")
                    
                    if red_flags:
                        st.warning(f"**{len(red_flags)} Red Flags Detected:**")
                        for i, flag in enumerate(red_flags[:7], 1):
                            st.markdown(f"{i}. {flag}")
                    else:
                        st.success("✅ No obvious red flags detected")
                    
                    # AI insights
                    with st.expander(" AI Processing Details"):
                        st.write(f"**Original AI Score:** {debug['ai_score']:.1f}%")
                        st.write(f"**Adjusted Risk Score:** {debug['adjusted_risk']:.1f}%")
                        st.write(f"**Extracted Domains:** {', '.join(debug['extracted_domains']) if debug['extracted_domains'] else 'None'}")
                        st.code(clean_text, language=None)
            
            elif analyze_btn and not email_input:
                st.warning(" Please enter email text to analyze")
            else:
                st.info(" **Get Started:**\n\n1. Paste email content in the left panel\n2. Click 'Analyze Email' button\n3. View detailed security analysis")
    
    with tab2:
        st.subheader("📊 Model Performance Statistics")
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.markdown("###  Model Metrics")
            st.metric("Test Accuracy", f"{config['test_accuracy']*100:.2f}%", delta="High Performance")
            st.metric("Vocabulary Size", f"{config['MAX_WORDS']:,}", delta="words")
            st.metric("Max Sequence Length", config['MAX_LENGTH'], delta="tokens")
            
        with col_stat2:
            st.markdown("###  Technology Stack")
            st.markdown("""
            - **Framework:** TensorFlow 2.x
            - **Architecture:** LSTM Neural Network
            - **NLP:** Advanced text preprocessing
            - **Domain Check:** Trusted sender verification
            - **Processing:** Real-time analysis
            """)
        
        st.markdown("---")
        st.markdown("###  Risk Level Classification")
        
        col_risk1, col_risk2, col_risk3 = st.columns(3)
        
        with col_risk1:
            st.markdown("""
            <div class="risk-high" style="padding: 15px;">
                <h3>🔴 HIGH RISK</h3>
                <p><strong>70-100%</strong></p>
                <p>Likely phishing attempt</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_risk2:
            st.markdown("""
            <div class="risk-medium" style="padding: 15px;">
                <h3>🟡 MEDIUM RISK</h3>
                <p><strong>40-70%</strong></p>
                <p>Exercise caution</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_risk3:
            st.markdown("""
            <div class="risk-low" style="padding: 15px;">
                <h3>🟢 LOW RISK</h3>
                <p><strong>0-40%</strong></p>
                <p>Appears legitimate</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("ℹ️ About CyberNova Guard")
        
        st.markdown("""
        ###  What is Phishing?
        
        Phishing is a cybersecurity attack where criminals impersonate legitimate organizations 
        to steal sensitive information like passwords, credit card numbers, or personal data.
        
        ###  How This Tool Works
        
        1. **Text Analysis:** AI processes email content using NLP
        2. **Pattern Recognition:** Identifies suspicious patterns and keywords
        3. **Domain Verification:** Checks sender against trusted sources
        4. **Risk Calculation:** Provides detailed threat assessment
        
        ###  Security Features
        
        - ✅ Real-time email scanning
        - ✅ AI-powered threat detection
        - ✅ Red flag identification
        - ✅ Domain trust verification
        - ✅ Detailed risk analysis
        - ✅ Privacy-focused (no data storage)
        
        ### 💡 Protection Tips
        
        1. **Verify Sender:** Check email addresses carefully
        2. **Hover Over Links:** Don't click suspicious URLs
        3. **Check Grammar:** Phishing emails often have errors
        4. **Be Skeptical:** If it seems too good to be true, it probably is
        5. **Use 2FA:** Enable two-factor authentication
        6. **Report Phishing:** Forward suspicious emails to your IT team
        
        ###  Part of CyberNova Guard Suite
        
        This module is one of four security tools:
        -  Email Phishing Detection *(You are here)*
        -  Password Breach Scanner
        -  Password Strength Checker
        -  WiFi Security Analyzer
        """)
    
    
    with st.sidebar:
        # 🔙 Back to Home button (TOP LEFT in sidebar)
        if st.button("⬅ Back"):
            st.session_state.current_module = None
            st.rerun()
    
        st.markdown("---")

        st.markdown("### Catch Phish Before They Catch You")
        
        
        st.markdown("---")
        
        st.markdown("###  Quick Stats")
        st.metric("Emails Analyzed", "Real-time")
        st.metric("Model Version", "v1.0")
        st.metric("Status", "🟢 Active")
        
        st.markdown("---")
        
        st.markdown("###  Common Phishing Signs")
        st.markdown("""
        -  Urgent action required
        -  Unexpected prizes/money
        -  Suspicious links
        -  Mismatched sender
        -  Requests for passwords
        -  Unexpected attachments
        -  Poor grammar/spelling
        """)
        
        st.markdown("---")
        st.caption("Built for Cybersecurity Education")
        st.caption("Detecting Threats, Protecting Trust")

if __name__ == "__main__":
    main()