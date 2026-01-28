import streamlit as st
import re
import math
import hashlib
import string
from datetime import timedelta
import base64

# Page ki congig
st.set_page_config(
    page_title="Password Strength Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

def set_bg(image_file):
    try:
        with open(image_file, "rb") as f:
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
            background: rgba(0,0,0,0.75);
            z-index: 0;
        }}
        .stApp > div {{
            position: relative;
            z-index: 1;
        }}
        
        /* sidebar ki styling */
        section[data-testid="stSidebar"] {{
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            width: 21rem !important;
            min-width: 21rem !important;
            max-width: 21rem !important;
            background: linear-gradient(180deg, rgba(5,5,20,0.98), rgba(15,5,30,0.98)) !important;
            border-right: 3px solid rgba(0,255,255,0.4) !important;
            box-shadow: 5px 0 30px rgba(0,255,255,0.2) !important;
            z-index: 999990 !important;
        }}
        
        section[data-testid="stSidebar"][aria-expanded="false"] {{
            margin-left: -21rem !important;
        }}
        
        section[data-testid="stSidebar"][aria-expanded="true"] {{
            margin-left: 0 !important;
        }}
        
        section[data-testid="stSidebar"] > div:first-child {{
            background: transparent !important;
            padding: 2rem 1rem !important;
        }}
        
        /* Header style */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 0px !important;
            padding: 0 !important;
        }}
  
        button[kind="header"] svg {{
            color: #00ffff !important;
            filter: drop-shadow(0 0 5px rgba(0,255,255,0.8)) !important;
        }}
        
        /* text color sidebar ka */
        section[data-testid="stSidebar"] * {{
            color: #ffffff !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        }}
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {{
            color: #00ffff !important;
            text-shadow: 0 0 15px rgba(0,255,255,0.7), 2px 2px 5px rgba(0,0,0,1) !important;
        }}
        
        /* sidebar k button */
        section[data-testid="stSidebar"] .stButton>button {{
            background: linear-gradient(135deg, #0a4d68, #1a7d9c) !important;
            color: #00ffff !important;
            border: 2px solid rgba(0,255,255,0.5) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.3) !important;
            transition: all 0.3s ease !important;
        }}
        
        section[data-testid="stSidebar"] .stButton>button:hover {{
            box-shadow: 0 0 25px rgba(0,255,255,0.6) !important;
            background: linear-gradient(135deg, #1a6d8c, #2a8dac) !important;
            transform: translateY(-2px) !important;
        }}
      
        /* Main titale ka styling */
        h1 {{
            font-weight: 700;
            color: #00ffff !important;
            text-shadow: 0 0 20px rgba(0,255,255,0.8), 2px 2px 8px rgba(0,0,0,1);
            background: linear-gradient(135deg, rgba(0,20,40,0.95), rgba(20,0,60,0.95)) !important;
            padding: 15px 30px !important;
            border-radius: 12px !important;
            border: 2px solid rgba(0,255,255,0.4) !important;
            box-shadow: 0 0 30px rgba(0,255,255,0.3);
            font-size: 2rem !important;
            text-align: center !important;
            width: fit-content !important;
            margin-left: auto !important;
            margin-right: auto !important;
            margin-bottom: 20px !important;
        }}

        /* Ain syb heading or baqi genrl txt color */
        h2, h3, h4, p, li, span, div {{
            color: #ffffff !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
        }}
        
        /* INPUT BOX STYLING or centered jrny ka*/
        .stTextInput {{
            max-width: 800px !important;
            margin: 0 auto !important;
        }}
        
        .stTextInput > div > div > input {{
            background: linear-gradient(135deg, rgba(0,10,25,0.9), rgba(10,0,30,0.9)) !important;
            color: #00ffff !important;
            border: 2px solid rgba(0,255,255,0.4) !important;
            border-radius: 8px !important;
            font-size: 1.1rem !important;
            font-family: 'Courier New', monospace !important;
            padding: 12px 16px !important;
            height: 50px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.2) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border: 2px solid rgba(0,255,255,0.8) !important;
            box-shadow: 0 0 25px rgba(0,255,255,0.4) !important;
        }}
        
        /* buton ki styling */
        .stButton > button {{
            background: linear-gradient(135deg, #0a4d68, #1a7d9c) !important;
            color: #00ffff !important;
            border: 2px solid rgba(0,255,255,0.5) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.3) !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 0 25px rgba(0,255,255,0.6) !important;
            background: linear-gradient(135deg, #1a6d8c, #2a8dac) !important;
            transform: translateY(-2px) !important;
        }}
        
        /* PROGRESS BAR STYLING */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, #ff0000, #ff8c00, #ffff00, #7fff00, #00ff00) !important;
            box-shadow: 0 0 10px rgba(0,255,255,0.6);
            border-radius: 10px !important;
        }}
        
        /* METRIC STYLING */
        [data-testid="stMetricValue"] {{
            color: #00ffff !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            text-shadow: 0 0 10px rgba(0,255,255,0.5) !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: #ffffff !important;
            font-size: 1rem !important;
        }}
        
        /* INFO BOX STYLING */
        .stAlert {{
            background: linear-gradient(135deg, rgba(0,20,40,0.8), rgba(0,40,80,0.8)) !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.2) !important;
        }}
        
        /* code block ki styling*/
        code {{
            background: linear-gradient(135deg, rgba(0,20,40,0.9), rgba(20,0,60,0.9)) !important;
            color: #00ff00 !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }}
        
        /* Divider ya line ki styling*/
        hr {{
            border-color: rgba(0,255,255,0.3) !important;
            box-shadow: 0 0 10px rgba(0,255,255,0.2) !important;
        }}
        
        /* SLIDER STYLING */
        .stSlider > div > div > div {{
            background: rgba(0,255,255,0.2) !important;
        }}
        
        .stSlider > div > div > div > div {{
            background: #00ffff !important;
            box-shadow: 0 0 10px rgba(0,255,255,0.5) !important;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    except:
        pass

# Background picture load 
set_bg("bg.jpg")

from pathlib import Path
import requests
import gzip
from io import BytesIO
@st.cache_resource
def load_common_passwords():
    """
    Load a rockyou-style list from an online GitHub raw file.
    The limit parameter prevents memory issues.
    """
    url = "https://github.com/josuamarcelc/common-password-list/raw/refs/heads/main/rockyou_2025_00.txt"
    passwords = set()

    try:
        with st.spinner("📥 Downloading password list..."):
            r = requests.get(url, stream=True, timeout=30)
            r.raise_for_status()

            for i, line in enumerate(r.iter_lines(decode_unicode=True)):
                if line:
                    passwords.add(line.strip().lower())
                if i <0:
                    break

        st.sidebar.success(f"✅ Loaded {len(passwords):,} passwords from online list")
        return passwords

    except Exception as e:
        st.sidebar.error(f"❌ Failed to load online password list: {e}")
        return None

# Common password patterns
COMMON_PATTERNS = {
    'keyboard': ['qwerty', 'asdfgh', 'zxcvbn', 'qwertz', 'azerty'],
    'sequential': ['123', '234', '345', '456', '567', '678', '789', 'abc', 'bcd', 'cde'],
    'repeated': ['111', '222', '333', '444', '555', '666', '777', '888', '999', '000', 'aaa', 'bbb'],
    'common_words': ['password', 'admin', 'user', 'login', 'welcome', 'hello', 'test'],
    'dates': ['2020', '2021', '2022', '2023', '2024', '2025', '1990', '1991', '1992', '1993', '1994', '1995']
}

def calculate_entropy(password):
    """Calculate password entropy (randomness)"""
    charset_size = 0
    
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 32
    
    if charset_size == 0:
        return 0
    
    entropy = len(password) * math.log2(charset_size)
    return entropy

def detect_patterns(password):
    """Detect common patterns in password"""
    issues = []
    pwd_lower = password.lower()
    
    # Check for keyboard patterns
    for pattern in COMMON_PATTERNS['keyboard']:
        if pattern in pwd_lower:
            issues.append(f"Contains keyboard pattern '{pattern}'")
    
    # Check for sequential charcters
    for pattern in COMMON_PATTERNS['sequential']:
        if pattern in pwd_lower:
            issues.append(f"Contains sequential pattern '{pattern}'")
    
    # Check for repeated chrcters
    for pattern in COMMON_PATTERNS['repeated']:
        if pattern in pwd_lower:
            issues.append(f"Contains repeated pattern '{pattern}'")
    
    # Check for commmon words
    for word in COMMON_PATTERNS['common_words']:
        if word in pwd_lower:
            issues.append(f"Contains common word '{word}'")
    
    # Check for dates
    for date in COMMON_PATTERNS['dates']:
        if date in password:
            issues.append(f"Contains date pattern '{date}'")
    
    # Check for name + number pattern
    if re.match(r'^[A-Z][a-z]+[a-z]+\d+$', password):
        issues.append("Predictable pattern: Name + Numbers")
    
    # Check for repeated charcters
    if re.search(r'(.)\1{2,}', password):
        issues.append("Contains 3+ repeated characters")
    
    # Check for simple Capitalization
    if len(password) > 1 and password[0].isupper() and password[1:].islower() and password[-1].isdigit():
        issues.append("Simple capitalization pattern detected")
    
    return issues

def calculate_crack_time(password, in_dictionary=False):
    """Calculate time to crack password"""
    
    if in_dictionary:
        return "Instant", "Already in breach databases", 0
    
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 32
    
    if charset_size == 0:
        return "Instant", "Invalid password", 0
    
    combinations = charset_size ** len(password)
    guesses_per_second = 100_000_000_000
    seconds = combinations / (2 * guesses_per_second)
    
    patterns = detect_patterns(password)
    if patterns:
        seconds = seconds / (10 ** len(patterns))
    
    if seconds < 1:
        return "Instant", "< 1 second", seconds
    elif seconds < 60:
        return f"{seconds:.1f} seconds", f"{seconds:.1f} seconds", seconds
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes", f"{minutes:.1f} minutes", seconds
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} hours", f"{hours:.1f} hours", seconds
    elif seconds < 2592000:
        days = seconds / 86400
        return f"{days:.1f} days", f"{days:.1f} days", seconds
    elif seconds < 31536000:
        months = seconds / 2592000
        return f"{months:.1f} months", f"{months:.1f} months", seconds
    elif seconds < 3153600000:
        years = seconds / 31536000
        return f"{years:.1f} years", f"{years:.1f} years", seconds
    else:
        centuries = seconds / 3153600000
        return f"{centuries:.1f} centuries", "Centuries", seconds

def analyze_password(password, common_passwords):
    """Complete password analysis"""
    
    if not password:
        return None
    
    analysis = {
        'length': len(password),
        'has_upper': bool(re.search(r'[A-Z]', password)),
        'has_lower': bool(re.search(r'[a-z]', password)),
        'has_digit': bool(re.search(r'[0-9]', password)),
        'has_special': bool(re.search(r'[^a-zA-Z0-9]', password)),
        'entropy': calculate_entropy(password),
        'patterns': detect_patterns(password),
        'in_dictionary': False,
        'score': 0
    }
    
    if common_passwords:
        analysis['in_dictionary'] = password.lower() in common_passwords
    
    score = 0
    
    if analysis['length'] >= 16:
        score += 30
    elif analysis['length'] >= 12:
        score += 20
    elif analysis['length'] >= 8:
        score += 10
    else:
        score += max(0, analysis['length'] * 1.5)
    
    if analysis['has_upper']:
        score += 10
    if analysis['has_lower']:
        score += 10
    if analysis['has_digit']:
        score += 10
    if analysis['has_special']:
        score += 10
    
    if analysis['entropy'] > 80:
        score += 20
    elif analysis['entropy'] > 60:
        score += 15
    elif analysis['entropy'] > 40:
        score += 10
    else:
        score += max(0, analysis['entropy'] / 4)
    
    score -= len(analysis['patterns']) * 10
    
    if analysis['in_dictionary']:
        score = min(score, 15)
    
    analysis['score'] = max(0, min(100, score))
    
    if analysis['score'] >= 80:
        analysis['strength'] = 'Excellent'
        analysis['color'] = '🟢'
        analysis['severity'] = 'LOW'
    elif analysis['score'] >= 60:
        analysis['strength'] = 'Strong'
        analysis['color'] = '🟢'
        analysis['severity'] = 'LOW'
    elif analysis['score'] >= 40:
        analysis['strength'] = 'Moderate'
        analysis['color'] = '🟡'
        analysis['severity'] = 'MEDIUM'
    elif analysis['score'] >= 20:
        analysis['strength'] = 'Weak'
        analysis['color'] = '🟠'
        analysis['severity'] = 'HIGH'
    else:
        analysis['strength'] = 'Critical'
        analysis['color'] = '🔴'
        analysis['severity'] = 'CRITICAL'
    
    crack_time, crack_desc, crack_seconds = calculate_crack_time(password, analysis['in_dictionary'])
    analysis['crack_time'] = crack_time
    analysis['crack_desc'] = crack_desc
    analysis['crack_seconds'] = crack_seconds
    
    return analysis

def generate_password(length=16):
    """Generate a strong random password"""
    import secrets
    
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password

def main():
    st.title(" Advanced Password Strength Analyzer")
    
    common_passwords = load_common_passwords()
    
    # Sidebar
    with st.sidebar:
        
        st.subheader(" Password Generator")
        gen_length = st.slider("Password Length", 8, 32, 16)
        
        if st.button("Generate Strong Password", use_container_width=True):
            generated = generate_password(gen_length)
            st.code(generated, language=None)
            st.caption("Click to copy →")
        
        st.markdown("---")
        st.subheader("📊 Database Info")
        if common_passwords:
            st.metric("Dictionary Size", f"{len(common_passwords):,}")
            st.caption("Loaded from password list")
        else:
            st.warning("No dictionary loaded")
        
        st.markdown("---")
        st.subheader("📈 Strength Levels")
        st.markdown("""
        - 🟢 **Excellent** (80-100%)
        - 🟢 **Strong** (60-79%)
        - 🟡 **Moderate** (40-59%)
        - 🟠 **Weak** (20-39%)
        - 🔴 **Critical** (0-19%)
        """)
    
    # Main content
    st.info(" **Quote** Complexity is your friend, predictability is your enemy in password creation.")
    
    st.markdown("###  Enter Password to Analyze")
    
    # Centered input with better layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password here...",
            label_visibility="collapsed"
        )
        
        analyze_btn = st.button(" Analyze Password", use_container_width=True, type="primary")
    
    # Real-time analysis
    if password:
        analysis = analyze_password(password, common_passwords)
        
        if analysis:
            st.markdown("---")
            st.markdown(f"### {analysis['color']} Password Strength: **{analysis['strength']}**")
            st.progress(analysis['score'] / 100)
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Score", f"{analysis['score']}/100")
            
            with col2:
                st.metric("Length", f"{analysis['length']} chars")
            
            with col3:
                st.metric("Entropy", f"{analysis['entropy']:.1f} bits")
            
            with col4:
                st.metric("Crack Time", analysis['crack_time'])
            
            st.markdown("---")
            
            # Detailed analysi
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ✅ Character Requirements")
                
                st.markdown(f"{'✅' if analysis['has_upper'] else '❌'} Uppercase letters (A-Z)")
                st.markdown(f"{'✅' if analysis['has_lower'] else '❌'} Lowercase letters (a-z)")
                st.markdown(f"{'✅' if analysis['has_digit'] else '❌'} Numbers (0-9)")
                st.markdown(f"{'✅' if analysis['has_special'] else '❌'} Special characters (!@#$...)")
                st.markdown(f"{'✅' if analysis['length'] >= 12 else '❌'} Minimum 12 characters")
                
                st.markdown("---")
                if analysis['in_dictionary']:
                    st.error(" **CRITICAL**: Found in breach database!")
                    st.caption(f"This password appears in known breaches ({len(common_passwords):,} passwords)")
                elif common_passwords:
                    st.success("✅ Not found in breach database")
                    st.caption(f"Checked against {len(common_passwords):,} known passwords")
            
            with col2:
                st.markdown("####  Security Analysis")
                
                if analysis['crack_seconds'] < 60:
                    st.error(f"🔴 **{analysis['crack_desc']}** to crack")
                    st.caption("Vulnerable to instant attacks")
                elif analysis['crack_seconds'] < 86400:
                    st.warning(f"🟡 **{analysis['crack_desc']}** to crack")
                    st.caption("Vulnerable to brute force")
                elif analysis['crack_seconds'] < 31536000:
                    st.info(f"🟢 **{analysis['crack_desc']}** to crack")
                    st.caption("Good resistance to attacks")
                else:
                    st.success(f"💎 **{analysis['crack_desc']}** to crack")
                    st.caption("Excellent resistance to attacks")
                
                st.markdown("---")
                
                if analysis['patterns']:
                    st.markdown("** Detected Patterns:**")
                    for pattern in analysis['patterns']:
                        st.markdown(f"- {pattern}")
                else:
                    st.success("✅ No common patterns detected")
            
            # Recommendatixns
            st.markdown("---")
            st.markdown("####  Recommendations")
            
            recommendations = []
            
            if analysis['score'] < 60:
                if not analysis['has_upper']:
                    recommendations.append("Add uppercase letters (A-Z)")
                if not analysis['has_lower']:
                    recommendations.append("Add lowercase letters (a-z)")
                if not analysis['has_digit']:
                    recommendations.append("Add numbers (0-9)")
                if not analysis['has_special']:
                    recommendations.append("Add special characters (!@#$%...)")
                if analysis['length'] < 12:
                    recommendations.append(f"Increase length to at least 12 characters (currently {analysis['length']})")
            
            if analysis['in_dictionary']:
                recommendations.append(" NEVER use this password - it's in breach databases!")
                recommendations.append("Generate a completely random password")
            
            if analysis['patterns']:
                recommendations.append("Avoid predictable patterns (keyboard sequences, dates, names+numbers)")
                recommendations.append("Use random combination of characters")
            
            if analysis['length'] < 16:
                recommendations.append("Consider using 16+ characters for maximum security")
            
            if not recommendations:
                recommendations = [
                    "✅ Excellent password!",
                    "Keep this password secure",
                    "Don't reuse it on other sites",
                    "Consider using a password manager"
                ]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
    
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ###  What We Check:
            - ✅ Length and complexity
            - ✅ Character variety
            - ✅ Common patterns
            - ✅ Dictionary words
            - ✅ Breach databases
            - ✅ Time to crack
            """)
        
        with col2:
            st.markdown("""
            ###  Best Practices:
            - Use 16+ characters
            - Mix upper, lower, numbers, symbols
            - Avoid personal info
            - Avoid common words
            - Use password manager
            - Unique per site
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #00ffff; text-shadow: 0 0 10px rgba(0,255,255,0.5);'>
             Advanced Password Strength Analyzer | Protect Your Digital Life
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()