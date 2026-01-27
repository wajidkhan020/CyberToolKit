import streamlit as st
import subprocess
import re
import platform
import pandas as pd
from datetime import datetime
import time
import streamlit as st
import base64
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    page_bg = f"""
    <style>

    /* --------------------------- Background Image --------------------------- */
    .stApp {{
        position: relative;
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* --------------------------- Dark Overlay --------------------------- */
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
/* --------------------------- HIDE HEADER BUT KEEP SIDEBAR TOGGLE --------------------------- */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0px !important;
        padding: 0 !important;
    }}
    

    button[kind="header"][data-testid="baseButton-header"]:hover {{
        background: rgba(0,150,200,0.9) !important;
        box-shadow: 0 0 15px rgba(0,255,255,0.5) !important;
    }}
    
    /* KEEP SIDEBAR VISIBLE */
    section[data-testid="stSidebar"] {{
        display: flex !important;
        visibility: visible !important;
    }}
    /* --------------------------- Title Box (WiFi Security Analyzer) --------------------------- */
    h1 {{
        font-weight: 700;
        color: #00ffff !important;
        text-shadow: 0 0 20px rgba(0,255,255,0.8), 2px 2px 8px rgba(0,0,0,1);
        background: linear-gradient(135deg, rgba(0,20,40,0.95), rgba(20,0,60,0.95)) !important;
        padding: 20px 30px !important;
        border-radius: 12px !important;
        border: 2px solid rgba(0,255,255,0.4) !important;
        box-shadow: 0 0 30px rgba(0,255,255,0.3), inset 0 0 20px rgba(0,100,150,0.2);
        display: inline-block;
        margin-bottom: 10px !important;
    }}

    h2, h3 {{
        font-weight: 700;
        color: #ffffff !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,1), 0 0 15px rgba(0,255,255,0.5);
    }}

    h2 {{
        font-size: 2.2rem !important;
    }}

    /* --------------------------- All Text --------------------------- */
    p, label, span, div {{
        font-size: 1.15rem !important;
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    }}

    /* --------------------------- Dark Cyber Boxes for Expanders --------------------------- */
    div[data-testid="stExpander"] {{
        background: linear-gradient(135deg, rgba(10,10,30,0.92), rgba(30,10,40,0.92)) !important;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(0,255,255,0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.7), 0 0 15px rgba(0,100,150,0.2);
    }}

    div[data-testid="stExpander"] summary {{
        color: #00ffff !important;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0,255,255,0.6);
    }}

    /* --------------------------- Metrics - Dark Cyber Box --------------------------- */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, rgba(0,10,25,0.95), rgba(10,0,30,0.95)) !important;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(0,255,255,0.4);
        box-shadow: 0 0 20px rgba(0,255,255,0.2), inset 0 0 15px rgba(0,50,100,0.3);
    }}

    div[data-testid="stMetricValue"] {{
        color: #00ffff !important;
        font-size: 2rem !important;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(0,255,255,0.9);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #88ddff !important;
    }}

    /* --------------------------- Buttons - Cyber Gradient --------------------------- */
    .stButton>button {{
        background: linear-gradient(135deg, #0a4d68, #1a6d8c, #0a4d68) !important;
        color: #00ffff !important;
        border: 2px solid rgba(0,255,255,0.5) !important;
        border-radius: 10px;
        padding: .7rem 1.4rem;
        font-size: 1.1rem !important;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(0,255,255,0.3);
        text-shadow: 0 0 10px rgba(0,255,255,0.8);
        transition: all 0.3s ease;
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(0,255,255,0.6);
        border-color: rgba(0,255,255,0.9) !important;
        background: linear-gradient(135deg, #1a6d8c, #2a8dac, #1a6d8c) !important;
    }}

    /* --------------------------- Sidebar - Dark Cyber --------------------------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(5,5,15,0.98), rgba(15,5,25,0.98)) !important;
        border-right: 2px solid rgba(0,255,255,0.3);
    }}

    section[data-testid="stSidebar"] * {{
        color: #ffffff !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }}

    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {{
        color: #00ffff !important;
        text-shadow: 0 0 15px rgba(0,255,255,0.7);
    }}

    /* --------------------------- Progress Bar - Cyber Glow --------------------------- */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #0a4d68, #00ffff, #0a4d68) !important;
        box-shadow: 0 0 10px rgba(0,255,255,0.6);
    }}

    /* --------------------------- Messages - Dark Cyber Boxes --------------------------- */
    .stSuccess, .stError, .stWarning, .stInfo {{
        background: linear-gradient(135deg, rgba(0,10,20,0.9), rgba(10,0,20,0.9)) !important;
        border-radius: 8px;
        padding: 15px;
        backdrop-filter: blur(8px);
    }}

    .stSuccess {{
        border: 2px solid rgba(0,255,100,0.6) !important;
        box-shadow: 0 0 15px rgba(0,255,100,0.3);
    }}

    .stError {{
        border: 2px solid rgba(255,50,50,0.6) !important;
        box-shadow: 0 0 15px rgba(255,50,50,0.3);
    }}

    .stWarning {{
        border: 2px solid rgba(255,200,0,0.6) !important;
        box-shadow: 0 0 15px rgba(255,200,0,0.3);
    }}

    .stInfo {{
        border: 2px solid rgba(0,200,255,0.6) !important;
        box-shadow: 0 0 15px rgba(0,200,255,0.3);
    }}

    /* --------------------------- Input Fields - Cyber Style --------------------------- */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div {{
        background: linear-gradient(135deg, rgba(0,10,25,0.9), rgba(10,0,30,0.9)) !important;
        color: #00ffff !important;
        border: 1px solid rgba(0,255,255,0.4) !important;
        border-radius: 6px;
        box-shadow: inset 0 0 10px rgba(0,100,150,0.3);
    }}

    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>div:focus {{
        border-color: rgba(0,255,255,0.8) !important;
        box-shadow: 0 0 15px rgba(0,255,255,0.4);
    }}

    /* --------------------------- Code Blocks - Dark Cyber --------------------------- */
    code {{
        background: linear-gradient(135deg, rgba(0,10,20,0.95), rgba(10,0,25,0.95)) !important;
        color: #00ffff !important;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid rgba(0,255,255,0.3);
        box-shadow: 0 0 10px rgba(0,255,255,0.2);
    }}

    /* --------------------------- Risk Score Glow --------------------------- */
    h1[style*="red"] {{
        color: #ff3333 !important;
        text-shadow: 0 0 30px rgba(255,50,50,1);
    }}

    h1[style*="orange"] {{
        color: #ff9933 !important;
        text-shadow: 0 0 30px rgba(255,150,50,1);
    }}

    h1[style*="yellow"] {{
        color: #ffdd33 !important;
        text-shadow: 0 0 30px rgba(255,220,50,1);
    }}

    h1[style*="green"] {{
        color: #33ff88 !important;
        text-shadow: 0 0 30px rgba(50,255,130,1);
    }}

    /* --------------------------- Tabs - Cyber Style --------------------------- */
    .stTabs [data-baseweb="tab-list"] {{
        background: linear-gradient(135deg, rgba(0,10,25,0.9), rgba(10,0,30,0.9));
        border-radius: 10px;
        padding: 5px;
        border: 1px solid rgba(0,255,255,0.3);
    }}

    .stTabs [data-baseweb="tab"] {{
        color: #88ddff !important;
        background: transparent;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(0,100,150,0.6), rgba(0,150,200,0.6)) !important;
        color: #00ffff !important;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0,255,255,0.4);
    }}

    /* --------------------------- Scrollbar - Cyber --------------------------- */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(0,10,20,0.5);
    }}

    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #0a4d68, #00ffff);
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,255,255,0.5);
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #1a6d8c, #00ffff);
    }}

    </style>
    """

    st.markdown(page_bg, unsafe_allow_html=True)

set_bg("bg.jpg")

class WiFiSecurityAnalyzer:

    def __init__(self):
        self.os_type = platform.system()
        
        # Vulnerability database
        self.encryption_risks = {
            "Open": {
                "severity": "CRITICAL",
                "risk_score": 100,
                "crack_time": "Instant (No encryption)",
                "color": "🔴",
                "description": "No encryption - All traffic visible to anyone nearby",
                "fix": "Never use for sensitive data. Use VPN if necessary."
            },
            "WEP": {
                "severity": "CRITICAL",
                "risk_score": 95,
                "crack_time": "5 minutes",
                "color": "🔴",
                "description": "Obsolete encryption with known vulnerabilities",
                "fix": "Upgrade router to WPA2/WPA3 immediately"
            },
            "WPA": {
                "severity": "HIGH",
                "risk_score": 75,
                "crack_time": "2-14 hours (with weak password)",
                "color": "🟡",
                "description": "Vulnerable to KRACK attack, outdated",
                "fix": "Upgrade to WPA2 or WPA3"
            },
            "WPA-PSK": {
                "severity": "HIGH",
                "risk_score": 70,
                "crack_time": "Hours to days",
                "color": "🟡",
                "description": "Old WPA version, vulnerable",
                "fix": "Upgrade to WPA2-PSK or WPA3"
            },
            "WPA2-Personal": {
                "severity": "MEDIUM",
                "risk_score": 35,
                "crack_time": "Days to months (weak password)",
                "color": "🟢",
                "description": "Good security if strong password used",
                "fix": "Use 16+ character random password, consider WPA3"
            },
            "WPA2-PSK": {
                "severity": "MEDIUM",
                "risk_score": 35,
                "crack_time": "Days to months (weak password)",
                "color": "🟢",
                "description": "Good security if strong password used",
                "fix": "Use 16+ character random password"
            },
            "WPA2": {
                "severity": "MEDIUM",
                "risk_score": 30,
                "crack_time": "Months to years (strong password)",
                "color": "🟢",
                "description": "Good encryption standard",
                "fix": "Ensure strong password, consider WPA3 upgrade"
            },
            "WPA2-Enterprise": {
                "severity": "LOW",
                "risk_score": 20,
                "crack_time": "Years (with proper setup)",
                "color": "🟢",
                "description": "Enterprise-grade security with authentication server",
                "fix": "Ensure certificates are up to date"
            },
            "WPA3": {
                "severity": "LOW",
                "risk_score": 10,
                "crack_time": "Years with strong password",
                "color": "🟢",
                "description": "Latest and most secure WiFi encryption",
                "fix": "Excellent security - ensure all devices support WPA3"
            },
            "WPA3-Personal": {
                "severity": "LOW",
                "risk_score": 10,
                "crack_time": "Years with strong password",
                "color": "🟢",
                "description": "Latest and most secure WiFi encryption",
                "fix": "Excellent security"
            }
        }
        
        # Default router names jo k baatye router ki setting unchanged hy
        self.default_names = [
            "NETGEAR", "Linksys", "TP-LINK", "TP-Link", "TPLINK",
            "D-Link", "Dlink", "ASUS", "Belkin", "default",
            "Wireless", "Router", "Home", "MyWiFi"
        ]
        
        # Suspicious keywords
        self.suspicious_keywords = ["free", "public", "guest", "open"]
    
    def scan_networks(self):

        try:
            if self.os_type == "Windows":
                return self._scan_windows()
            else:
                return []
        except Exception as e:
            st.error(f"Scan failed: {str(e)}")
            return []
    
    def _scan_windows(self):
        """Scan networks on Windows using netsh"""
        try:
            result = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                timeout=10
            )
            
            networks = []
            current_network = {}
            
            for line in result.split('\n'):
                line = line.strip()
                
                if line.startswith('SSID') and ':' in line:
                    if current_network and current_network.get('ssid'):
                        networks.append(current_network)
                    ssid = line.split(':', 1)[1].strip()
                    current_network = {'ssid': ssid if ssid else 'Hidden Network'}
                    
                elif 'Authentication' in line and ':' in line:
                    auth = line.split(':', 1)[1].strip()
                    current_network['encryption'] = auth
                    
                elif 'Signal' in line and ':' in line:
                    signal = line.split(':', 1)[1].strip()
                    current_network['signal'] = signal
                    
                elif 'BSSID' in line and ':' in line:
                    bssid = line.split(':', 1)[1].strip()
                    current_network['bssid'] = bssid
                    
                elif 'Channel' in line and ':' in line:
                    channel = line.split(':', 1)[1].strip()
                    current_network['channel'] = channel
            
            if current_network and current_network.get('ssid'):
                networks.append(current_network)
            
            return networks
            
        except subprocess.TimeoutExpired:
            st.error("Scan timeout - taking too long")
            return []
        except Exception as e:
            st.error(f"Windows scan error: {str(e)}")
            return []
    def analyze_network(self, network):
        """
        Analyze individual network security
        """
        ssid = network.get('ssid', 'Unknown')
        encryption = network.get('encryption', 'Unknown')
        signal = network.get('signal', '0%')
        bssid = network.get('bssid', 'Unknown')
        
        # Encryption type batye ga
        enc_type = self._determine_encryption_type(encryption)
        
        # Get base vulnerability info
        vuln_info = self.encryption_risks.get(enc_type, {
            "severity": "UNKNOWN",
            "risk_score": 50,
            "crack_time": "Unknown",
            "color": "⚪",
            "description": "Unknown encryption type",
            "fix": "Verify router settings"
        })
        
        risk_score = vuln_info['risk_score']
        warnings = []
        recommendations = []
        
        # Add base warning
        if vuln_info['severity'] != "LOW":
            warnings.append(f"{vuln_info['color']} {vuln_info['description']}")
        
        # dafoul router name chk kry ga
        if any(default in ssid for default in self.default_names):
            risk_score += 10
            warnings.append("⚠️ Default router name detected - likely default password too")
            recommendations.append("Change router name and password")
        
        # Check for suspicious keywords
        ssid_lower = ssid.lower()
        for keyword in self.suspicious_keywords:
            if keyword in ssid_lower:
                risk_score += 15
                warnings.append(f"⚠️ Public/Free network keyword: '{keyword}'")
                recommendations.append("Don't use for sensitive transactions")
                break
        
        # Check signal strength anomaly
        try:
            signal_num = int(signal.replace('%', ''))
            if signal_num > 90:
                risk_score += 2
                warnings.append("⚠️ Unusually strong signal - verify legitimate network")
        except:
            pass
        
        # Add recommendations
        if not recommendations:
            recommendations.append(vuln_info['fix'])
        
        return {
            "ssid": ssid,
            "bssid": bssid,
            "encryption": enc_type,
            "raw_encryption": encryption,
            "signal": signal,
            "channel": network.get('channel', 'Unknown'),
            "risk_score": min(risk_score, 100),
            "severity": self._calculate_severity(min(risk_score, 100)),
            "crack_time": vuln_info['crack_time'],
            "color": vuln_info['color'],
            "warnings": warnings,
            "recommendations": recommendations,
            "verdict": self._get_verdict(min(risk_score, 100))
        }
    
    def _determine_encryption_type(self, encryption):
        """Determine encryption type from raw string"""
        enc = encryption.upper()
        
        if 'WPA3' in enc:
            return 'WPA3-Personal' if 'PERSONAL' in enc else 'WPA3'
        elif 'WPA2' in enc:
            if 'ENTERPRISE' in enc:
                return 'WPA2-Enterprise'
            elif 'PERSONAL' in enc or 'PSK' in enc:
                return 'WPA2-Personal'
            else:
                return 'WPA2'
        elif 'WPA' in enc and 'PSK' in enc:
            return 'WPA-PSK'
        elif 'WPA' in enc:
            return 'WPA'
        elif 'WEP' in enc:
            return 'WEP'
        elif 'OPEN' in enc or enc == '' or 'NONE' in enc:
            return 'Open'
        else:
            return encryption
    
    def _calculate_severity(self, risk_score):
        """Calculate severity level"""
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_verdict(self, risk_score):
        """Get security verdict"""
        if risk_score >= 80:
            return "🔴 DANGEROUS - DO NOT USE"
        elif risk_score >= 60:
            return "🟠 HIGH RISK - Avoid if possible"
        elif risk_score >= 40:
            return "🟡 MODERATE - Use with caution"
        elif risk_score >= 20:
            return "🟢 GOOD - Generally safe"
        else:
            return "✅ EXCELLENT - Very secure"
    
    def detect_evil_twins(self, networks):
        """
        Detect possible evil twin attacks (duplicate SSIDs)
        """
        ssid_groups = {}
        
        for network in networks:
            ssid = network.get('ssid', 'Unknown')
            if ssid and ssid != 'Hidden Network':
                if ssid not in ssid_groups:
                    ssid_groups[ssid] = []
                ssid_groups[ssid].append(network)
        
        evil_twins = []
        for ssid, group in ssid_groups.items():
            if len(group) > 1:
                # Multiple networks with same name!
                evil_twins.append({
                    "ssid": ssid,
                    "count": len(group),
                    "networks": group,
                    "warning": f" {len(group)} networks found with name '{ssid}'",
                    "advice": "One might be fake! Verify MAC address or ask network administrator."
                })
        
        return evil_twins


# Streamlit UI
def main():
    st.set_page_config(
        page_title="WiFi Security Analyzer",
        page_icon="📡",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title(" WiFi Security Analyzer")
    st.markdown("**Real-time WiFi Security Analysis**")
    st.markdown("Your WiFi password is the only thing standing between your data and every hacker within 300 feet.")
    st.markdown("---")
    
    # start kry ga anaylyzer ko
    analyzer = WiFiSecurityAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **WiFi Security Analyzer** helps you:
        -  Scan nearby WiFi networks
        -  Identify security vulnerabilities
        -  Detect evil twin attacks
        -  Get security recommendations
        
        **Encryption Types:**
        - 🔴 Open/WEP: Critical Risk
        - 🟡 WPA/WPA-PSK: High Risk
        - 🟢 WPA2: Good Security
        - ✅ WPA3: Best Security
        """)
        
        st.markdown("---")
        st.info(f"**OS Detected:** {analyzer.os_type}")
        st.caption("🔒 This tool only scans publicly broadcast information. It does NOT hack or attack networks.")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(" Network Scanner")
        
        if st.button("🔄 Scan WiFi Networks", type="primary", use_container_width=True):
            with st.spinner("Scanning for WiFi networks... Please wait..."):
                # Show scanning animation
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                networks = analyzer.scan_networks()
                
                if networks:
                    st.session_state['networks'] = networks
                    st.session_state['scan_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success(f"✅ Found {len(networks)} networks!")
                else:
                    st.error("❌ No networks found. Make sure WiFi is enabled.")
    
    with col2:
        if 'networks' in st.session_state:
            st.metric("Networks Found", len(st.session_state['networks']))
            st.metric("Last Scan", st.session_state.get('scan_time', 'Never'))
    
    # Display results
    if 'networks' in st.session_state:
        networks = st.session_state['networks']
        
        st.markdown("---")
        st.subheader("📊 Security Analysis Results")
        
        # Analyze all networks
        analyzed_networks = [analyzer.analyze_network(net) for net in networks]
        
        # Sort by risk score (highest first)
        analyzed_networks.sort(key=lambda x: x['risk_score'], reverse=True)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        critical_count = sum(1 for net in analyzed_networks if net['severity'] == 'CRITICAL')
        high_count = sum(1 for net in analyzed_networks if net['severity'] == 'HIGH')
        medium_count = sum(1 for net in analyzed_networks if net['severity'] == 'MEDIUM')
        low_count = sum(1 for net in analyzed_networks if net['severity'] == 'LOW')
        
        col1.metric("🔴 Critical", critical_count)
        col2.metric("🟠 High Risk", high_count)
        col3.metric("🟡 Medium", medium_count)
        col4.metric("🟢 Low Risk", low_count)
        
        # Evil Twin Detection
        st.markdown("---")
        evil_twins = analyzer.detect_evil_twins(networks)
        
        if evil_twins:
            st.error("🚨 **EVIL TWIN ATTACK DETECTED!**")
            for twin in evil_twins:
                with st.expander(f" {twin['warning']}", expanded=True):
                    st.warning(twin['advice'])
                    for i, network in enumerate(twin['networks'], 1):
                        st.write(f"**Network {i}:**")
                        st.write(f"- MAC Address: `{network.get('bssid', 'Unknown')}`")
                        st.write(f"- Signal Strength: {network.get('signal', 'Unknown')}")
                        st.write(f"- Encryption: {network.get('encryption', 'Unknown')}")
                    st.markdown("**Recommendation:** Verify the correct MAC address with the network administrator before connecting.")
        
        # Detailed Network Analysis
        st.markdown("---")
        st.subheader("📡 Detailed Network Information")
        
        # Filter options
        filter_option = st.selectbox(
            "Filter by severity:",
            ["All Networks", "Critical Only", "High Risk Only", "Medium Risk", "Low Risk"]
        )
        
        # Apply filter
        if filter_option == "Critical Only":
            filtered_networks = [net for net in analyzed_networks if net['severity'] == 'CRITICAL']
        elif filter_option == "High Risk Only":
            filtered_networks = [net for net in analyzed_networks if net['severity'] == 'HIGH']
        elif filter_option == "Medium Risk":
            filtered_networks = [net for net in analyzed_networks if net['severity'] == 'MEDIUM']
        elif filter_option == "Low Risk":
            filtered_networks = [net for net in analyzed_networks if net['severity'] == 'LOW']
        else:
            filtered_networks = analyzed_networks
        
        # Display each network
        for network in filtered_networks:
            risk_color = "red" if network['risk_score'] >= 80 else "orange" if network['risk_score'] >= 60 else "yellow" if network['risk_score'] >= 40 else "green"
            
            with st.expander(f"{network['color']} **{network['ssid']}** - {network['verdict']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Security Details:**")
                    st.write(f"- Encryption: `{network['encryption']}`")
                    st.write(f"- Signal Strength: {network['signal']}")
                    st.write(f"- MAC Address: `{network['bssid']}`")
                    st.write(f"- Channel: {network['channel']}")
                    st.write(f"- Can be cracked in: **{network['crack_time']}**")
                    
                    if network['warnings']:
                        st.markdown("**⚠️ Security Issues:**")
                        for warning in network['warnings']:
                            st.write(f"- {warning}")
                    
                    if network['recommendations']:
                        st.markdown("**✅ Recommendations:**")
                        for rec in network['recommendations']:
                            st.write(f"- {rec}")
                
                with col2:
                    st.markdown(f"**Risk Score:**")
                    st.progress(network['risk_score'] / 100)
                    st.markdown(f"<h1 style='text-align: center; color: {risk_color};'>{network['risk_score']}/100</h1>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'><strong>Severity: {network['severity']}</strong></p>", unsafe_allow_html=True)
        
        # Export option
        st.markdown("---")
        if st.button("📥 Export Results as CSV"):
            df = pd.DataFrame([{
                "Network Name": net['ssid'],
                "Encryption": net['encryption'],
                "Signal": net['signal'],
                "Risk Score": net['risk_score'],
                "Severity": net['severity'],
                "Verdict": net['verdict']
            } for net in analyzed_networks])
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"wifi_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def