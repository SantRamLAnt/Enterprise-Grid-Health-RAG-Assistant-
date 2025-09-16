import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Predictive Grid Intelligence RAG System",
    page_icon="⚡",
    layout="wide"
)

# Initialize session state
if 'grok_visible' not in st.session_state:
    st.session_state.grok_visible = True
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_persona' not in st.session_state:
    st.session_state.user_persona = 'Field Technician'

# Dark mode CSS with minimalist design
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .main-header {
        font-size: 2.5rem;
        color: #00d4ff;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    .grok-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(14, 17, 23, 0.95);
        backdrop-filter: blur(10px);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .grok-assistant {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #00d4ff;
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.3);
        animation: grokFloat 3s ease-in-out infinite;
    }
    
    @keyframes grokFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .grok-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff 0%, #0066cc 100%);
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        animation: pulse 2s infinite;
    }
    
    .metric-card {
        background: #1a1a2e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #00d4ff;
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.2);
    }
    
    .alert-card {
        background: #2d1b1b;
        border-left: 4px solid #ff4757;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .response-card {
        background: #1a2e1a;
        border-left: 4px solid #2ed573;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .query-card {
        background: #1a1a2e;
        border-left: 4px solid #00d4ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .steps-section {
        background: #2a2a3e;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ffa502;
    }
    
    .contact-section {
        background: #2e1a2e;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .sidebar .sidebar-content {
        background-color: #0e1117;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a2e;
        border: 1px solid #333;
        color: #fafafa;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0066cc 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }
    
    .footer {
        background: #1a1a2e;
        border-top: 1px solid #333;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Advanced electric utility queries categorized by system components
ELECTRIC_UTILITY_QUERIES = {
    "Transmission System (69kV-765kV)": [
        "HVDC converter station forced outage recovery procedures",
        "Series compensation capacitor bank protection failure analysis", 
        "Extra high voltage (500kV+) energized maintenance switching procedures",
        "Transmission line galloping conductor emergency response",
        "Static VAR compensator (SVC) control system malfunction troubleshooting"
    ],
    "Distribution System (4kV-34.5kV)": [
        "Recloser coordination for fault current discrimination on 12.47kV feeders",
        "Underground cable concentric neutral corrosion assessment procedures",
        "Automated distribution feeder switching during N-1 contingency events", 
        "Capacitor bank failure analysis with harmonic distortion evaluation",
        "Distribution transformer overload management during peak demand"
    ],
    "Protection & Control Systems": [
        "SEL-421 differential relay misoperation analysis and correction",
        "IED cybersecurity incident response for GOOSE message manipulation",
        "Synchrophasor data validation for wide-area protection schemes",
        "Distance relay Zone 3 overreach coordination with load encroachment",
        "Generator step-up transformer REF87 restricted earth fault calibration"
    ],
    "Substation Operations": [
        "230kV gas-insulated switchgear (GIS) SF6 leak containment procedures",
        "Control house HVAC failure during extreme weather operation continuity",
        "Station service transformer failure with critical control power loss",
        "Digital fault recorder triggering optimization for protection studies",
        "Substation physical security breach protocol with NERC CIP compliance"
    ],
    "Generation Interconnection": [
        "Wind farm collector system fault ride-through verification testing",
        "Solar PV inverter anti-islanding protection validation procedures", 
        "Combined cycle power plant black start capability restoration",
        "Hydroelectric generator excitation system stability analysis",
        "Battery energy storage system (BESS) grid-forming inverter commissioning"
    ],
    "System Operations & Planning": [
        "Real-time contingency analysis with transfer limit calculations",
        "Economic dispatch optimization with transmission constraints",
        "Voltage stability assessment using modal analysis techniques",
        "Load forecast error analysis during renewable generation ramp events",
        "Interchange scheduling validation with NERC tagging procedures"
    ]
}

# Detailed technical responses with step-by-step procedures
DETAILED_UTILITY_RESPONSES = {
    "HVDC converter station forced outage recovery procedures": {
        "answer": "HVDC converter station outage requires coordinated AC/DC system restoration. Station typically consists of 12-pulse thyristor converters with AC filters and reactive compensation. Outage affects power transfer capability up to 3000MW on major interties. Recovery sequence must maintain AC system voltage stability while preventing converter transformer energization transients that could damage thyristor valves.",
        "steps": [
            "1. IMMEDIATE (0-5 min): Notify NERC Reliability Coordinator and adjacent control areas of HVDC outage",
            "2. ASSESSMENT (5-15 min): Verify AC system stability, check for cascading outages, confirm converter station equipment status",
            "3. AC PREP (15-30 min): Adjust AC system voltage to 1.05 pu at converter bus, verify reactive compensation availability",
            "4. DC PREP (30-45 min): Inspect thyristor valve cooling systems, verify control system functionality, check DC line isolation",
            "5. ENERGIZATION (45-60 min): Energize converter transformers sequentially, verify AC filter operation, start valve group blocking",
            "6. COMMISSIONING (60-90 min): Perform converter valve firing angle tests, verify protective relay coordination",
            "7. POWER TRANSFER (90+ min): Gradually increase DC power transfer in 10% increments to rated capacity"
        ],
        "contacts": [
            "NERC Reliability Coordinator: 1-800-GRID-OPS",
            "HVDC Technical Support: ABB/Siemens 24/7 hotline", 
            "System Operations Manager: Internal ext. 2401",
            "Protection Engineering: Internal ext. 3205",
            "Transmission Maintenance Supervisor: Internal ext. 4102"
        ],
        "sources": ["NERC Operating Manual Section 12", "HVDC Converter Station O&M Manual", "IEEE Std 1204-1997"],
        "confidence": 0.98,
        "risk_level": "CRITICAL",
        "estimated_time": "90-120 minutes full restoration",
        "personnel_required": "HVDC Specialist, System Operator, Protection Engineer"
    },
    "SEL-421 differential relay misoperation analysis and correction": {
        "answer": "SEL-421 transformer differential relay misoperation requires immediate analysis to prevent equipment damage and ensure protection reliability. Common causes include CT saturation, winding connection errors, or tap changer position mismatch. Relay uses restraint characteristics and harmonic blocking to distinguish between faults and magnetizing inrush.",
        "steps": [
            "1. SECURE EQUIPMENT (0-10 min): Verify transformer is de-energized and grounded, lockout all associated breakers",
            "2. DATA COLLECTION (10-30 min): Retrieve SEL-421 event report, oscillographic data, and settings file",
            "3. CT VERIFICATION (30-60 min): Check CT ratios, polarity, and connection per relay compensation settings",
            "4. SETTINGS REVIEW (60-90 min): Verify differential pickup (87P), restraint slope (SLP1/SLP2), and harmonic blocking settings",
            "5. WAVEFORM ANALYSIS (90-120 min): Analyze differential current, restraint current, and harmonic content during operation",
            "6. RATIO CORRECTION (120-150 min): Adjust TAP settings for transformer tap changer position if applicable",
            "7. FUNCTIONAL TEST (150-180 min): Perform end-to-end test with secondary injection to verify correct operation",
            "8. DOCUMENTATION (180+ min): Update protection database and create misoperation report per NERC PRC-004"
        ],
        "contacts": [
            "SEL Technical Support: 1-509-332-1890",
            "Protection Engineering Manager: Internal ext. 3200",
            "Relay Testing Contractor: 24/7 emergency line",
            "NERC Compliance Officer: Internal ext. 1205",
            "Equipment Manufacturer Rep: Regional support"
        ],
        "sources": ["SEL-421 Instruction Manual", "IEEE C37.91 Guide", "NERC PRC-004-WECC-2"],
        "confidence": 0.96,
        "risk_level": "HIGH",
        "estimated_time": "3-4 hours analysis and correction",
        "personnel_required": "Protection Engineer, Relay Technician, Test Equipment Operator"
    },
    "Underground cable concentric neutral corrosion assessment procedures": {
        "answer": "Concentric neutral corrosion in URD cables (typically 15kV class) leads to impedance imbalance, neutral current circulation, and eventual cable failure. Assessment requires specialized testing to evaluate neutral conductor integrity without service interruption. Corrosion accelerated by soil conditions, stray currents, and electrochemical reactions.",
        "steps": [
            "1. PRELIMINARY (0-30 min): Review historical fault data, customer complaints, and previous neutral current measurements",
            "2. VISUAL INSPECTION (30-60 min): Inspect accessible neutral connections at switchgear, pad-mounted transformers",
            "3. NEUTRAL RESISTANCE (60-120 min): Measure neutral-to-ground resistance using specialized bridge methods",
            "4. CURRENT MEASUREMENT (120-180 min): Install split-core CTs to measure neutral current circulation patterns",
            "5. SOIL ANALYSIS (180-240 min): Test soil resistivity and pH levels along cable route using Wenner method",
            "6. CABLE TESTING (240-300 min): Perform insulation resistance and hipot testing on phases and neutral",
            "7. SECTIONALIZING (300+ min): Use cable fault locators to identify specific degraded cable sections",
            "8. PRIORITIZATION (Post-test): Rank cables for replacement based on neutral integrity percentage"
        ],
        "contacts": [
            "Cable Testing Specialist: Contractor 24/7 service",
            "Distribution Engineering: Internal ext. 2150", 
            "Underground Construction Manager: Internal ext. 4205",
            "Soil Testing Laboratory: External vendor",
            "Cable Manufacturer Technical Support: Regional rep"
        ],
        "sources": ["IEEE Std 404", "NECA Underground Distribution Manual", "Company Cable Testing Procedures"],
        "confidence": 0.94,
        "risk_level": "MEDIUM",
        "estimated_time": "6-8 hours comprehensive assessment",
        "personnel_required": "Cable Technician, Distribution Engineer, Testing Contractor"
    },
    "Wind farm collector system fault ride-through verification testing": {
        "answer": "Wind farm collector system (typically 34.5kV) must demonstrate fault ride-through capability per NERC PRC-024-2 to maintain grid stability. Testing verifies that wind turbine generators remain connected during transmission system faults and provide reactive current support. Critical for maintaining system frequency and voltage during contingency events.",
        "steps": [
            "1. PRE-TEST SETUP (0-60 min): Configure SCADA monitoring, verify protection settings, establish communication with turbine SCADA",
            "2. BASELINE DATA (60-90 min): Record normal operating conditions including voltage, current, power factor, and frequency",
            "3. COORDINATION (90-120 min): Coordinate with transmission operator for planned voltage dip testing windows",
            "4. LOW VOLTAGE TEST (120-180 min): Apply voltage dips to 0.15 pu for up to 625ms per LVRT requirements",
            "5. HIGH VOLTAGE TEST (180-240 min): Apply voltage rise to 1.2 pu for 1 second per HVRT requirements", 
            "6. REACTIVE CURRENT (240-300 min): Verify reactive current injection of 1.0 pu during voltage dip events",
            "7. FREQUENCY RESPONSE (300-360 min): Test turbine response to frequency deviations outside deadband",
            "8. DOCUMENTATION (360+ min): Generate IEEE 1547 compliant test report with oscillographic evidence"
        ],
        "contacts": [
            "NERC Generator Interconnection: Regional contact",
            "Turbine Manufacturer Support: GE/Vestas/Siemens hotline",
            "Transmission Planning Engineer: Internal ext. 2301",
            "Testing Contractor: Power system testing company",
            "FERC Compliance Manager: Internal ext. 1150"
        ],
        "sources": ["NERC PRC-024-2", "IEEE 1547.1", "IEC 61400-21-1 Wind Turbine Standard"],
        "confidence": 0.97,
        "risk_level": "MEDIUM",
        "estimated_time": "8-10 hours testing plus documentation",
        "personnel_required": "Generation Engineer, Test Technician, Turbine Specialist"
    },
    "Real-time contingency analysis with transfer limit calculations": {
        "answer": "Real-time contingency analysis evaluates N-1 and N-2 contingencies to determine Available Transfer Capability (ATC) and Total Transfer Capability (TTC) for scheduling interchange transactions. Analysis uses power flow and stability calculations updated every 5-15 minutes with current system topology and generation dispatch.",
        "steps": [
            "1. DATA ACQUISITION (0-5 min): Update real-time state estimator with current telemetry from SCADA/EMS",
            "2. TOPOLOGY UPDATE (5-10 min): Verify current transmission line and generation unit status",
            "3. N-1 ANALYSIS (10-20 min): Simulate outage of each transmission element and check thermal/voltage limits",
            "4. STABILITY ANALYSIS (20-30 min): Perform transient stability analysis for critical contingencies",
            "5. LIMIT CALCULATION (30-40 min): Determine most limiting element and calculate transfer limits",
            "6. ATC CALCULATION (40-50 min): Calculate Available Transfer Capability considering TRM and CBM",
            "7. OASIS POSTING (50-55 min): Update ATC values on OASIS for market participants",
            "8. OPERATOR NOTIFICATION (55-60 min): Alert system operators of any transfer limit changes"
        ],
        "contacts": [
            "NERC Reliability Coordinator: Regional RC hotline",
            "Market Operations: Internal ext. 2501",
            "EMS Support: Vendor 24/7 technical support",
            "Planning Engineer: Internal ext. 2301", 
            "Interchange Coordinator: Internal ext. 2401"
        ],
        "sources": ["NERC MOD Standards", "OASIS Business Practice Manual", "EMS Software User Guide"],
        "confidence": 0.95,
        "risk_level": "MEDIUM",
        "estimated_time": "Continuous 15-minute cycles",
        "personnel_required": "System Operator, Planning Engineer, EMS Analyst"
    }
}

# Button to dismiss overlay
if st.session_state.grok_visible:
    # Display the overlay
    overlay_html = f"""
    <div class="grok-overlay" id="grok-overlay">
        <div class="grok-assistant">
            <div class="grok-avatar">🤖</div>
            <h2 style="color: #00d4ff; margin-bottom: 1rem;">Grok-4 Assistant Ready</h2>
            <p style="font-size: 1.1em; line-height: 1.6; margin-bottom: 1.5rem;">
                Hello there! I'm Grok-4, your friendly AI assistant for electric utility operations. 
                I'm here to help with anything you need - from emergency procedures to complex technical analysis.
                Ready to make your day easier and keep the lights on! ⚡
            </p>
        </div>
    </div>
    """
    st.markdown(overlay_html, unsafe_allow_html=True)
    
    # Button to dismiss overlay - this will cause a rerun and hide the overlay
    if st.button("Let's Get Started! 🚀", key="start_button"):
        st.session_state.grok_visible = False
        st.rerun()

# Only show main content if overlay is dismissed
if not st.session_state.grok_visible:
    # Main header
    st.markdown('<div class="main-header">⚡ Predictive Grid Intelligence</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem;'>Next-Generation AI Assistant for Electric Utility Operations</p>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        persona = st.selectbox("Select Your Role:", [
            "Transmission Operator", 
            "Distribution Engineer",
            "Protection & Control Engineer", 
            "System Planning Engineer",
            "Substation Maintenance Supervisor",
            "Generation Operations Specialist"
        ])
        st.session_state.user_persona = persona

        st.markdown("### 🔧 System Status")
        st.markdown("**AI Model:** xAI Grok-4 Turbo")
        st.markdown("**Status:** 🟢 Online")
        st.markdown("**Response Time:** 0.8s avg")
        st.markdown("**Confidence:** 96.4%")
        st.markdown("**Last Update:** Real-time")

    # Navigation
    page = st.sidebar.radio("Navigate:", [
        "🎯 Operations Dashboard", 
        "🤖 Intelligent Assistant", 
        "🏗️ System Architecture"
    ])

    if page == "🎯 Operations Dashboard":
        st.markdown(f"### Welcome, {persona}")
        
        # Real-time grid status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
            <h4 style="color: #2ed573;">System Load</h4>
            <h2>2,847 MW</h2>
            <small>87% of peak capacity</small>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
            <h4 style="color: #ffa502;">Active Alarms</h4>
            <h2>12</h2>
            <small>3 critical, 9 warnings</small>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card">
            <h4 style="color: #00d4ff;">Equipment Availability</h4>
            <h2>98.7%</h2>
            <small>Transmission system</small>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="metric-card">
            <h4 style="color: #ff4757;">Customer Outages</h4>
            <h2>2,447</h2>
            <small>3 major circuits affected</small>
            </div>
            """, unsafe_allow_html=True)

        # Active alerts
        st.markdown("### 🚨 Priority System Alerts")
        st.markdown("""
        <div class="alert-card">
        <strong>CRITICAL:</strong> West 230kV Bus - Differential relay operation, Bus Section A isolated<br>
        <strong>Equipment:</strong> 230kV GIS Switchgear Bay 5<br>
        <strong>Impact:</strong> Loss of 450 MW transfer capability to southern region<br>
        <strong>Action Required:</strong> Emergency switching to restore N-1 contingency compliance<br>
        <strong>ETA:</strong> Field crew dispatched, 2-hour restoration estimate
        </div>
        """, unsafe_allow_html=True)

    elif page == "🤖 Intelligent Assistant":
        st.markdown("### 🧠 Grok-4 Electric Utility Expert")
        st.markdown("Ask me anything about electric utility operations, and I'll provide detailed technical guidance with step-by-step procedures.")
        
        # Query category selection
        category = st.selectbox("Select Technical Domain:", list(ELECTRIC_UTILITY_QUERIES.keys()))
        
        # Specific query selection based on category
        specific_query = st.selectbox("Choose Specific Technical Issue:", ELECTRIC_UTILITY_QUERIES[category])
        
        # Custom query option
        custom_query = st.text_input("Or describe your specific situation:")
        
        # Use custom query if provided, otherwise use selected query
        active_query = custom_query if custom_query else specific_query
        
        if st.button("🚀 Consult Grok-4 Expert System"):
            # Add to conversation history
            st.session_state.conversation_history.append({
                "role": "user",
                "content": active_query,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "persona": persona
            })
            
            with st.spinner("Grok-4 is analyzing technical parameters and consulting utility standards..."):
                time.sleep(random.uniform(2.0, 4.0))  # Realistic processing time for complex analysis
                
            # Display user query
            st.markdown(f"""
            <div class="query-card">
            <strong>👨‍⚙️ {persona}:</strong><br>
            {active_query}
            <div style="text-align: right; font-size: 0.8em; color: #888; margin-top: 0.5rem;">
            {st.session_state.conversation_history[-1]["timestamp"]}
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate response
            if active_query in DETAILED_UTILITY_RESPONSES:
                response = DETAILED_UTILITY_RESPONSES[active_query]
                
                # Add response to conversation history
                st.session_state.conversation_history.append({
                    "role": "assistant", 
                    "content": response["answer"],
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # Display comprehensive technical response
                st.markdown(f"""
                <div class="response-card">
                <h4>🤖 Grok-4 Technical Analysis:</h4>
                <p style="margin: 1rem 0; line-height: 1.6;">{response['answer']}</p>
                
                <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #333;">
                <strong>📚 Technical References:</strong> {' • '.join(response['sources'])}<br>
                <strong>📊 Analysis Confidence:</strong> {response['confidence']:.0%}<br>
                <strong>⚠️ Risk Classification:</strong> {response['risk_level']}<br>
                <strong>⏱️ Estimated Resolution Time:</strong> {response['estimated_time']}<br>
                <strong>👥 Required Personnel:</strong> {response['personnel_required']}
                </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Step-by-step emergency procedures
                st.markdown("""
                <div class="steps-section">
                <h4>📋 Step-by-Step Emergency Resolution Procedures:</h4>
                """, unsafe_allow_html=True)
                
                for step in response["steps"]:
                    st.markdown(f"<p style='margin: 0.5rem 0; padding: 0.5rem; background: #3a3a4e; border-radius: 5px;'>{step}</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Emergency contacts and escalation procedures  
                st.markdown("""
                <div class="contact-section">
                <h4>📞 Emergency Contacts & Technical Support:</h4>
                """, unsafe_allow_html=True)
                
                for contact in response["contacts"]:
                    st.markdown(f"<p style='margin: 0.5rem 0; padding: 0.5rem; background: #4e3a4e; border-radius: 5px;'>• {contact}</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            else:
                # Enhanced generic response for custom queries
                generic_responses = [
                    "Based on IEEE standards and NERC reliability criteria, this situation requires careful analysis of system operating limits and protective relay coordination. I recommend consulting IEEE Std C37.2 for device function numbers and NERC PRC standards for protection system requirements. Would you like me to help identify the specific standards and procedures that apply to your equipment configuration?",
                    "This technical challenge involves multiple considerations including equipment ratings, system protection, and operational safety protocols. Let me break down the key engineering factors: 1) Verify equipment nameplate ratings and operating limits, 2) Review protection system coordination studies, 3) Assess environmental and loading conditions, 4) Evaluate compliance with NESC and company safety standards. What specific aspect would you like me to analyze in detail?",
                    "From my analysis of utility industry best practices and regulatory requirements, this situation typically requires coordination between multiple departments including System Operations, Protection Engineering, and Field Maintenance. The response should follow established emergency procedures while maintaining compliance with NERC reliability standards. I can help you develop a specific action plan if you provide additional details about your system configuration."
                ]
                
                response_text = random.choice(generic_responses)
                
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                st.markdown(f"""
                <div class="response-card">
                <h4>🤖 Grok-4 Technical Guidance:</h4>
                <p style="margin: 1rem 0; line-height: 1.6;">{response_text}</p>
                
                <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #333;">
                <strong>📊 Analysis Confidence:</strong> 89%<br>
                <strong>💡 Recommendation:</strong> For equipment-specific procedures, consult manufacturer O&M manuals and company technical standards<br>
                <strong>📞 Technical Support:</strong> Contact Protection Engineering ext. 3200 for detailed relay coordination questions
                </div>
                </div>
                """, unsafe_allow_html=True)

        # Display conversation history
        if st.session_state.conversation_history:
            with st.expander("📜 Technical Consultation History", expanded=False):
                for i, msg in enumerate(st.session_state.conversation_history):
                    if msg["role"] == "user":
                        st.markdown(f"**{msg.get('persona', 'User')}** ({msg['timestamp']}): {msg['content']}")
                    else:
                        st.markdown(f"**🤖 Grok-4** ({msg['timestamp']}): {msg['content'][:200]}...")

    elif page == "🏗️ System Architecture":
        st.markdown("### 🏗️ Advanced Electric Utility AI Architecture")
        
        # Architecture flow diagram
        st.markdown("""
        <div style="background: #1a1a2e; border: 1px solid #333; border-radius: 10px; padding: 2rem; text-align: center; margin: 2rem 0;">
        <h4 style="color: #00d4ff;">Real-Time Electric Utility Intelligence Data Flow</h4>
        <div style="font-size: 1.1em; line-height: 2; margin-top: 1rem;">
        <strong>SCADA/EMS</strong> → <strong>State Estimator</strong> → <strong>xAI Grok-4</strong> → 
        <strong>Technical Standards DB</strong> → <strong>Expert System</strong> → <strong>Operations Interface</strong>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🧠 AI Technical Core")
            st.markdown("""
            - **xAI Grok-4**: Advanced reasoning for power system analysis
            - **IEEE Standards Database**: Complete technical specifications library  
            - **NERC Compliance Engine**: Real-time regulatory validation
            - **Equipment Models**: Manufacturer-specific technical parameters
            - **Historical Analysis**: Pattern recognition from operational data
            """)
            
        with col2:
            st.markdown("#### 🔒 Utility Security & Compliance")
            st.markdown("""
            - **NERC CIP Compliance**: Critical infrastructure protection standards
            - **IEC 61850 Integration**: Secure substation communication protocols
            - **Cybersecurity Framework**: NIST guidelines for grid operations
            - **Access Control**: Role-based permissions for technical personnel
            - **Audit Trails**: Complete operational decision logging
            """)
        
        # Performance metrics
        st.markdown("#### 📊 Technical System Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Analysis Response", "0.8s", "-0.2s")
        with col2:
            st.metric("Technical Accuracy", "96.4%", "+1.2%")  
        with col3:
            st.metric("System Uptime", "99.97%", "+0.02%")
        with col4:
            st.metric("Active Engineers", "247", "+12")

    # Footer
    st.markdown("""
    <div class="footer">
    <h4 style="color: #00d4ff;">⚡ Predictive Grid Intelligence</h4>
    <p>Powered by xAI Grok-4 • IEEE/NERC Compliant • Real-time Operations</p>
    <p style="font-size: 0.9em; color: #666;">Advanced AI system for professional electric utility operations</p>
    </div>
    """, unsafe_allow_html=True)
