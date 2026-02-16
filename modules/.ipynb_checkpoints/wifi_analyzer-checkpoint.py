import streamlit as st
import re
import socket
import ssl
import requests
from urllib.parse import urlparse
from datetime import datetime, timedelta
import json
import base64
import whois

# Suspicious TLDs commonly used for phishing
SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', 
    '.work', '.click', '.link', '.stream', '.download', '.win'
]

# Phishing keywords
PHISHING_KEYWORDS = [
    'verify', 'account', 'suspend', 'security', 'update', 'confirm',
    'login', 'signin', 'banking', 'paypal', 'amazon', 'secure',
    'wallet', 'crypto', 'prize', 'winner', 'claim', 'urgent'
]

# Trusted domains
TRUSTED_DOMAINS = [
    'google.com', 'facebook.com', 'youtube.com', 'amazon.com',
    'microsoft.com', 'apple.com', 'twitter.com', 'instagram.com',
    'linkedin.com', 'github.com', 'stackoverflow.com', 'wikipedia.org'
]

# Common typosquatting patterns
TYPOSQUAT_PATTERNS = {
    'google': ['g00gle', 'gooogle', 'googel', 'gogle'],
    'facebook': ['faceb00k', 'facebok', 'faceboook'],
    'paypal': ['paypai', 'paypa1', 'paypall'],
    'amazon': ['amaz0n', 'amazom', 'arnazon'],
    'microsoft': ['micr0soft', 'microsft', 'miscrosoft']
}

def set_bg(image_file):
    """Set background image"""
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
        section[data-testid="stSidebar"] > div:first-child {{
            background: transparent !important;
            padding: 2rem 1rem !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            max-height: 100vh !important;
        }}
        /* Hide sidebar collapse button */
        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}
        
        [data-testid="stSidebarHeader"] {{
            display: none !important;
        }}
        
        /* Custom scrollbar for sidebar */
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {{
            width: 8px !important;
        }}
        
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track {{
            background: rgba(0,0,0,0.3) !important;
            border-radius: 10px !important;
        }}
        
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {{
            background: rgba(0,255,255,0.5) !important;
            border-radius: 10px !important;
        }}
        
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {{
            background: rgba(0,255,255,0.8) !important;
        }}
        
        /* Make sure main content can scroll */
        .main .block-container {{
            overflow-y: auto !important;
            max-height: 100vh !important;
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
        /* ADD THESE LINES HERE - Hide sidebar collapse arrow */
        button[kind="header"] {{
            display: none !important;
        }}
        
        section[data-testid="stSidebar"][aria-expanded="false"] {{
            margin-left: 0 !important;
        }}
        
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
        /* Main title styling */
        h1 {{
            font-weight: 700;
            color: #00ffff !important;
            text-shadow: 0 0 20px rgba(0,255,255,0.8), 2px 2px 8px rgba(0,0,0,1);
            background: linear-gradient(135deg, rgba(0,20,40,0.95), rgba(20,0,60,0.95)) !important;
            padding: 15px 30px !important;
            border-radius: 12px !important;
            border: 2px solid rgba(0,255,255,0.4) !important;
            box-shadow: 0 0 30px rgba(0,255,255,0.3);
            text-align: center !important;
        }}

        h2, h3, h4, p, li, span, div {{
            color: #ffffff !important;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
        }}
        
        /* Input styling */
        .stTextInput > div > div > input {{
            background: linear-gradient(135deg, rgba(0,10,25,0.9), rgba(10,0,30,0.9)) !important;
            color: #00ffff !important;
            border: 2px solid rgba(0,255,255,0.4) !important;
            border-radius: 8px !important;
            font-size: 1.1rem !important;
            padding: 12px 16px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.2) !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border: 2px solid rgba(0,255,255,0.8) !important;
            box-shadow: 0 0 25px rgba(0,255,255,0.4) !important;
        }}
        
        /* Button styling */
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
        
        # .stButton > button:hover {{
        #     box-shadow: 0 0 25px rgba(0,255,255,0.6) !important;
        #     background: linear-gradient(135deg, #1a6d8c, #2a8dac) !important;
        #     transform: translateY(-2px) !important;
        }}
        
        /* Progress bar */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, #ff0000, #ff8c00, #ffff00, #7fff00, #00ff00) !important;
            box-shadow: 0 0 10px rgba(0,255,255,0.6);
            border-radius: 10px !important;
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            color: #00ffff !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            text-shadow: 0 0 10px rgba(0,255,255,0.5) !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: #ffff !important;
        }}
        
        /* Alert boxes */
        .stAlert {{
            background: linear-gradient(135deg, rgba(0,20,40,0.8), rgba(0,40,80,0.8)) !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 15px rgba(0,255,255,0.2) !important;
        }}
        
        /* Code blocks */
        code {{
            background: linear-gradient(135deg, rgba(0,20,40,0.9), rgba(20,0,60,0.9)) !important;
            color: #00ff00 !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            border: 1px solid rgba(0,255,255,0.3) !important;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    except:
        pass

def validate_url(url):
    """Validate and normalize URL"""
    if not url:
        return None, "URL cannot be empty"
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return None, "Invalid URL format"
        return url, None
    except:
        return None, "Invalid URL format"

def get_domain_info(domain):
    """Get WHOIS information for domain"""
    try:
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':')[0]
        
        w = whois.whois(domain)
        
        # Handle dates
        creation_date = w.creation_date
        expiration_date = w.expiration_date
        updated_date = w.updated_date
        
        # WHOIS sometimes returns lists, get first element
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if isinstance(updated_date, list):
            updated_date = updated_date[0]
        
        # Calculate domain age
        domain_age_days = 0
        if creation_date:
            domain_age_days = (datetime.now() - creation_date).days
        
        # Get registrar
        registrar = w.registrar if hasattr(w, 'registrar') else 'Unknown'
        
        # Get name servers
        name_servers = w.name_servers if hasattr(w, 'name_servers') else []
        if isinstance(name_servers, list):
            name_servers = name_servers[:3]  # Limit to 3
        
        return {
            'found': True,
            'creation_date': creation_date.strftime('%Y-%m-%d') if creation_date else 'Unknown',
            'expiration_date': expiration_date.strftime('%Y-%m-%d') if expiration_date else 'Unknown',
            'updated_date': updated_date.strftime('%Y-%m-%d') if updated_date else 'Unknown',
            'domain_age_days': domain_age_days,
            'registrar': registrar,
            'name_servers': name_servers,
            'creation_date_obj': creation_date,
            'expiration_date_obj': expiration_date
        }
    except Exception as e:
        return {
            'found': False,
            'error': str(e),
            'creation_date': 'Unable to fetch',
            'expiration_date': 'Unable to fetch',
            'domain_age_days': 0
        }

def check_ssl_certificate(url):
    """Check SSL certificate validity"""
    try:
        parsed = urlparse(url)
        hostname = parsed.netloc
        
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Get certificate info
                issued_to = dict(x[0] for x in cert['subject'])
                issued_by = dict(x[0] for x in cert['issuer'])
                
                # Check expiry
                expire_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_to_expire = (expire_date - datetime.now()).days
                
                return {
                    'valid': True,
                    'issued_to': issued_to.get('commonName', 'Unknown'),
                    'issued_by': issued_by.get('organizationName', 'Unknown'),
                    'expires': expire_date.strftime('%Y-%m-%d'),
                    'days_to_expire': days_to_expire,
                    'version': cert['version']
                }
    except ssl.SSLError:
        return {'valid': False, 'error': 'SSL Certificate Error'}
    except socket.timeout:
        return {'valid': False, 'error': 'Connection Timeout'}
    except:
        return {'valid': False, 'error': 'Could not verify certificate'}

def detect_typosquatting(domain):
    """Detect typosquatting attempts"""
    domain_lower = domain.lower()
    detected = []
    
    for legit, typos in TYPOSQUAT_PATTERNS.items():
        for typo in typos:
            if typo in domain_lower:
                detected.append(f"Possible typosquatting of '{legit}' (found '{typo}')")
    
    # Check for number substitutions
    if re.search(r'[0-9]', domain):
        common_subs = {'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's'}
        for num, letter in common_subs.items():
            if num in domain_lower:
                detected.append(f"Suspicious number substitution: '{num}' (might be '{letter}')")
    
    return detected

def analyze_url_patterns(url, domain_info=None):
    """Analyze URL for suspicious patterns"""
    issues = []
    score = 100
    
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    full_url = url.lower()
    
    # Check protocol
    if not url.startswith('https://'):
        issues.append("⚠️ Not using HTTPS (insecure)")
        score -= 20
    
    # Check for IP address instead of domain
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
        issues.append("🔴 Using IP address instead of domain name (highly suspicious)")
        score -= 30
    
    # Check suspicious TLDs
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            issues.append(f"⚠️ Suspicious TLD: {tld} (commonly used for phishing)")
            score -= 25
            break
    
    # Check for phishing keywords
    found_keywords = []
    for keyword in PHISHING_KEYWORDS:
        if keyword in full_url:
            found_keywords.append(keyword)
    
    if found_keywords:
        issues.append(f"⚠️ Phishing keywords found: {', '.join(found_keywords[:3])}")
        score -= len(found_keywords) * 5
    
    # Check for typosquatting
    typosquat = detect_typosquatting(domain)
    if typosquat:
        issues.extend(typosquat)
        score -= 30
    
    # Check domain age if available
    if domain_info and domain_info.get('found'):
        age_days = domain_info.get('domain_age_days', 0)
        if age_days < 30:
            issues.append(f"🔴 Very new domain ({age_days} days old) - HIGH RISK")
            score -= 40
        elif age_days < 180:
            issues.append(f"⚠️ Recently registered domain ({age_days} days old)")
            score -= 20
        elif age_days > 365:
            # Bonus for older domains
            score = min(100, score + 10)
    
    # Check for suspicious patterns
    if '@' in full_url:
        issues.append("🔴 '@' symbol in URL (credential phishing attempt)")
        score -= 35
    
    # Check for excessive subdomains
    subdomain_count = domain.count('.') - 1
    if subdomain_count > 3:
        issues.append(f"⚠️ Excessive subdomains ({subdomain_count}) - suspicious")
        score -= 15
    
    # Check for double extensions
    if re.search(r'\.(exe|zip|apk|bat)\.(com|net|org)', path):
        issues.append("🔴 Double file extension detected (malware indicator)")
        score -= 40
    
    # Check for very long URLs
    if len(url) > 200:
        issues.append("⚠️ Extremely long URL (obfuscation attempt)")
        score -= 10
    
    # Check for trusted domains
    is_trusted = False
    for trusted in TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith('.' + trusted):
            is_trusted = True
            score = min(100, score + 20)
            break
    
    return {
        'score': max(0, score),
        'issues': issues,
        'is_trusted': is_trusted
    }

def check_redirects(url):
    """Check for redirect chains"""
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        
        if len(response.history) > 0:
            redirect_chain = [r.url for r in response.history]
            redirect_chain.append(response.url)
            return {
                'has_redirects': True,
                'count': len(response.history),
                'chain': redirect_chain,
                'final_url': response.url
            }
        else:
            return {
                'has_redirects': False,
                'count': 0,
                'final_url': url
            }
    except:
        return {'error': 'Could not check redirects'}

def get_safety_level(score):
    """Determine safety level based on score"""
    if score >= 80:
        return {
            'level': 'SAFE',
            'color': '🟢',
            'emoji': '✅',
            'recommendation': 'This URL appears safe to visit.',
            'bg_color': '#1a5928'
        }
    elif score >= 60:
        return {
            'level': 'LIKELY SAFE',
            'color': '🟡',
            'emoji': '✓',
            'recommendation': 'Exercise caution. Some minor concerns detected.',
            'bg_color': '#8b8000'
        }
    elif score >= 40:
        return {
            'level': 'SUSPICIOUS',
            'color': '🟠',
            'emoji': '⚠️',
            'recommendation': 'Be very careful. Multiple security concerns found.',
            'bg_color': '#8b4000'
        }
    else:
        return {
            'level': 'DANGEROUS',
            'color': '🔴',
            'emoji': '❌',
            'recommendation': 'DO NOT VISIT! High probability of phishing/malware.',
            'bg_color': '#8b0000'
        }

def main():
    """Main function for URL Safety Checker"""
    
    # Set background
    set_bg("bg.jpg")
    
    st.title("🌐 Advanced URL Safety Checker")
    
    # Sidebar info
    with st.sidebar:
     # 🔙 Back to Home button (TOP LEFT in sidebar)
        if st.button("⬅ Back"):
            st.session_state.current_module = None
            st.rerun()
       
        st.markdown("---")
    
        st.subheader("🔍 What We Check")
        st.markdown("""
        - ✅ Domain registration date
        - ✅ Domain age & expiry
        - ✅ SSL Certificate validity
        - ✅ Suspicious URL patterns
        - ✅ Phishing keywords
        - ✅ Typosquatting attempts
        - ✅ Malicious TLDs
        - ✅ Redirect chains
        - ✅ WHOIS information
        """)
        
        st.markdown("---")
        st.subheader("📊 Safety Levels")
        st.markdown("""
        - 🟢 **SAFE** (80-100)
        - 🟡 **LIKELY SAFE** (60-79)
        - 🟠 **SUSPICIOUS** (40-59)
        - 🔴 **DANGEROUS** (0-39)
        """)
        
        st.markdown("---")
        st.subheader("⚠️ Red Flags")
        st.markdown("""
        - Domain < 30 days old
        - No HTTPS encryption
        - Suspicious domain extensions
        - Typosquatting patterns
        - IP address URLs
        - Multiple redirects
        - Phishing keywords
        """)
        
        st.markdown("---")
        st.subheader("💡 Pro Tip")
        st.info("Domains less than 30 days old are HIGH RISK for phishing!")
    
    
    # Main content
    st.info("💡 **Tip**: Always verify URLs before clicking, especially in emails or messages!")
    
    st.markdown("### 🔗 Enter URL to Analyze")
    
    # URL input
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        url_input = st.text_input(
            "URL",
            placeholder="https://example.com or example.com",
            label_visibility="collapsed"
        )
        
        analyze_btn = st.button("🔍 Analyze URL", use_container_width=True, type="primary")
    
    # Analysis
    if url_input and analyze_btn:
        # Validate URL
        url, error = validate_url(url_input)
        
        if error:
            st.error(f"❌ {error}")
        else:
            with st.spinner("🔍 Analyzing URL security..."):
                parsed = urlparse(url)
                domain = parsed.netloc
                
                # Get domain info (WHOIS)
                domain_info = get_domain_info(domain)
                
                # Pattern analysis
                pattern_analysis = analyze_url_patterns(url, domain_info)
                
                # SSL check
                ssl_info = check_ssl_certificate(url)
                
                # Redirect check
                redirect_info = check_redirects(url)
                
                # Calculate final score
                final_score = pattern_analysis['score']
                
                # Adjust score based on SSL
                if ssl_info['valid']:
                    final_score = min(100, final_score + 10)
                else:
                    final_score = max(0, final_score - 20)
                
                # Adjust for redirects
                if redirect_info.get('count', 0) > 2:
                    final_score = max(0, final_score - 15)
                
                safety = get_safety_level(final_score)
            
            st.markdown("---")
            
            # Display results
            st.markdown(f"""
                <div style='background: {safety['bg_color']}; padding: 20px; border-radius: 10px; 
                            border: 2px solid rgba(255,255,255,0.3); margin: 20px 0;'>
                    <h2 style='text-align: center; margin: 0;'>
                        {safety['color']} {safety['level']}
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Score
            st.markdown(f"### {safety['emoji']} Safety Score: {final_score}/100")
            st.progress(final_score / 100)
            
            st.markdown(f"**Recommendation:** {safety['recommendation']}")
            
            st.markdown("---")
            
            # Detailed results in 3 columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🔒 SSL Certificate")
                if ssl_info['valid']:
                    st.success("✅ Valid SSL Certificate")
                    st.markdown(f"**Issued to:** {ssl_info.get('issued_to', 'N/A')}")
                    st.markdown(f"**Issued by:** {ssl_info.get('issued_by', 'N/A')}")
                    st.markdown(f"**Expires:** {ssl_info.get('expires', 'N/A')}")
                    
                    days = ssl_info.get('days_to_expire', 0)
                    if days < 30:
                        st.warning(f"⚠️ Expires in {days} days")
                    else:
                        st.info(f"Valid for {days} more days")
                else:
                    st.error(f"❌ {ssl_info.get('error', 'Invalid Certificate')}")
            
            with col2:
                st.markdown("#### 📅 Domain Information")
                if domain_info.get('found'):
                    # Registration date
                    st.markdown(f"**Registered:** {domain_info['creation_date']}")
                    
                    # Domain age
                    age_days = domain_info['domain_age_days']
                    if age_days > 0:
                        age_years = age_days // 365
                        age_months = (age_days % 365) // 30
                        
                        if age_years > 0:
                            age_str = f"{age_years} year(s), {age_months} month(s)"
                        else:
                            age_str = f"{age_months} month(s), {age_days % 30} day(s)"
                        
                        st.markdown(f"**Domain Age:** {age_str}")
                        
                        # Age indicator
                        if age_days < 30:
                            st.error("🔴 Very New Domain - HIGH RISK")
                        elif age_days < 180:
                            st.warning("⚠️ Recently Registered")
                        elif age_days < 365:
                            st.info("ℹ️ Less than 1 year old")
                        else:
                            st.success("✅ Established Domain")
                    
                    # Expiration date
                    st.markdown(f"**Expires:** {domain_info['expiration_date']}")
                    
                    # Registrar
                    st.markdown(f"**Registrar:** {domain_info.get('registrar', 'Unknown')}")
                    
                else:
                    st.warning("⚠️ Could not retrieve domain info")
                    st.caption(f"Reason: {domain_info.get('error', 'Unknown')}")
            
            with col3:
                st.markdown("#### 🔗 Redirect Analysis")
                if redirect_info.get('has_redirects'):
                    count = redirect_info['count']
                    if count > 2:
                        st.warning(f"⚠️ {count} redirects detected")
                    else:
                        st.info(f"ℹ️ {count} redirect(s)")
                    
                    with st.expander("View redirect chain"):
                        for i, redir_url in enumerate(redirect_info['chain'], 1):
                            st.code(f"{i}. {redir_url}")
                else:
                    st.success("✅ No redirects")
            
            # Security Issues
            st.markdown("---")
            st.markdown("#### ⚠️ Security Analysis")
            
            if pattern_analysis['issues']:
                for issue in pattern_analysis['issues']:
                    st.markdown(f"- {issue}")
            else:
                st.success("✅ No major security issues detected")
            
            if pattern_analysis['is_trusted']:
                st.success("✅ Domain is in trusted list")
            
            # Additional Domain Details
            if domain_info.get('found') and domain_info.get('name_servers'):
                st.markdown("---")
                st.markdown("#### 🌐 Name Servers")
                for ns in domain_info['name_servers']:
                    st.code(ns)
            
            # URL breakdown
            st.markdown("---")
            st.markdown("#### 🔍 URL Breakdown")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Protocol", parsed.scheme.upper())
            
            with col2:
                st.metric("Domain", parsed.netloc)
            
            with col3:
                st.metric("Path", parsed.path if parsed.path else "/")
            
            with col4:
                st.metric("Query", "Yes" if parsed.query else "No")
    
    else:
        # Example URLs
        st.markdown("---")
        st.markdown("### 📝 Try These Examples:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Safe URLs:**
            - `https://github.com`
            - `https://google.com`
            - `https://wikipedia.org`
            """)
        
        with col2:
            st.markdown("""
            **Suspicious Patterns:**
            - URLs with `.tk` or `.ml` domains
            - URLs with IP addresses
            - URLs with phishing keywords
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #00ffff; text-shadow: 0 0 10px rgba(0,255,255,0.5);'>
            🌐 Advanced URL Safety Checker | Stay Safe Online
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()