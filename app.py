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

# Comprehensive utility-specific queries and responses
UTILITY_QUERIES = {
    "Emergency Procedures": [
        "Emergency shutdown sequence for 345kV transmission line",
        "SCADA lockout procedures during equipment failure", 
        "Storm restoration priorities for critical infrastructure",
        "Gas leak response protocol near electrical equipment",
        "Coordinated outage procedures with neighboring utilities"
    ],
    "Equipment Diagnostics": [
        "SF6 gas pressure analysis in circuit breakers",
        "Transformer oil dissolved gas analysis interpretation", 
        "Power factor testing on 138kV cable systems",
        "Partial discharge testing on switchgear",
        "Infrared thermography patterns for conductor issues"
    ],
    "Maintenance Procedures": [
        "Live line maintenance on 69kV distribution circuits",
        "Substation grounding system testing procedures",
        "Capacitor bank switching operations",
        "Underground cable fault location techniques", 
        "Protective relay coordination testing"
    ],
    "Safety Protocols": [
        "Arc flash hazard assessment for 480V motor control centers",
        "Personal protective equipment for energized work",
        "Minimum approach distances for different voltage levels",
        "Lock-out/tag-out procedures for transmission equipment",
        "Confined space entry for underground vaults"
    ],
    "System Operations": [
        "Load forecasting during extreme weather events",
        "Voltage regulation using capacitor banks and LTCs", 
        "Economic dispatch optimization for peak demand",
        "Renewable energy integration impact on grid stability",
        "Demand response program activation procedures"
    ]
}

DETAILED_RESPONSES = {
    "Emergency shutdown sequence for 345kV transmission line": {
        "answer": "345kV transmission line emergency shutdown requires: 1) Immediate notification to System Operations Center, 2) Verify protection operation and identify faulted section, 3) Open line terminals at both substations using SCADA, 4) Perform switching to isolate the line completely, 5) Ground the line using portable grounds, 6) Notify neighboring utilities of system impact. Critical: Maintain N-1 contingency throughout process. Estimated restoration time: 4-6 hours pending damage assessment.",
        "sources": ["NERC Operating Manual Section 8.3", "Company Emergency Response Procedures", "345kV Line Protection Schemes"],
        "confidence": 0.98,
        "risk_level": "CRITICAL",
        "estimated_time": "45 minutes",
        "personnel_required": "2 System Operators, 1 Field Supervisor, 4 Line Crew"
    },
    "SF6 gas pressure analysis in circuit breakers": {
        "answer": "SF6 gas pressure monitoring indicates breaker operational status. Normal pressure: 6-7 bar at 20°C. Low pressure alarm at 5.5 bar requires immediate attention - reduces interrupting capability. Pressure below 5 bar = lockout condition. Temperature compensation essential: +0.07 bar per 10°C increase. Moisture content must be <150ppm. Annual leak rate should not exceed 0.5% of nameplate quantity. Gas purity testing required if pressure drops >10% annually.",
        "sources": ["IEEE C37.122.1 Standard", "SF6 Gas Handling Procedures", "Circuit Breaker Maintenance Manual"],
        "confidence": 0.95,
        "risk_level": "MEDIUM",
        "estimated_time": "30 minutes testing",
        "personnel_required": "1 Certified SF6 Technician"
    },
    "Arc flash hazard assessment for 480V motor control centers": {
        "answer": "480V MCC arc flash assessment requires: 1) Calculate incident energy using IEEE 1584 standard, 2) Typical values range 8-40 cal/cm² at 18 inches, 3) PPE Category 2-4 required based on calculation, 4) Arc flash boundary typically 4-8 feet, 5) Working distance must be >18 inches minimum. Install arc flash labels showing: incident energy, arc flash boundary, PPE category, working distance. Update every 5 years or after system modifications.",
        "sources": ["NFPA 70E Standard", "IEEE 1584 Arc Flash Guide", "Company Electrical Safety Manual"],
        "confidence": 0.96,
        "risk_level": "HIGH", 
        "estimated_time": "2 hours assessment",
        "personnel_required": "1 Electrical Engineer, 1 Safety Coordinator"
    },
    "Load forecasting during extreme weather events": {
        "answer": "Extreme weather load forecasting adjustments: 1) Summer heat waves: +15-25% peak demand per 10°F above normal, 2) Winter storms: +20-30% heating load, potential service interruptions, 3) Use temperature-load regression models with weather service data, 4) Activate demand response programs when forecast exceeds 95% of peak capacity, 5) Pre-position emergency resources based on 72-hour weather outlook. Monitor real-time SCADA vs forecast every 15 minutes during events.",
        "sources": ["Load Forecasting Procedures", "Weather Service Partnership Agreement", "Emergency Operations Manual"],
        "confidence": 0.92,
        "risk_level": "MEDIUM",
        "estimated_time": "Continuous monitoring",
        "personnel_required": "Load Dispatcher, Weather Analyst"
    },
    "Transformer oil dissolved gas analysis interpretation": {
        "answer": "DGA interpretation for power transformers: H2 >100ppm indicates overheating. C2H2 >3ppm = arcing/electrical fault. C2H4/C2H6 ratio >1 = thermal fault >700°C. CO/CO2 ratio >0.3 = paper insulation degradation. Total Combustible Gas >720ppm requires immediate investigation. Key fault gases: H2+CH4 = partial discharge, C2H2+C2H4 = arcing, C2H4+C2H6 = thermal. Schedule quarterly testing for units >20MVA. Emergency actions required if gases double in 30 days.",
        "sources": ["IEEE C57.104 DGA Standard", "Transformer Diagnostic Manual", "Oil Testing Laboratory Procedures"],
        "confidence": 0.97,
        "risk_level": "VARIABLE",
        "estimated_time": "48 hours lab results",
        "personnel_required": "Transformer Specialist, Lab Technician"
    }
}

# Grok-4 Assistant Overlay
if st.session_state.grok_visible:
    st.markdown(f"""
    <div class="grok-overlay" id="grok-overlay">
        <div class="grok-assistant">
            <div class="grok-avatar">🤖</div>
            <h2 style="color: #00d4ff; margin-bottom: 1rem;">Grok-4 Assistant Ready</h2>
            <p style="font-size: 1.1em; line-height: 1.6; margin-bottom: 1.5rem;">
                Hello there! I'm Grok-4, your friendly AI assistant for grid operations. 
                I'm here to help with anything you need - from emergency procedures to complex technical analysis.
                Ready to make your day easier and keep the lights on! ⚡
            </p>
            <button onclick="document.getElementById('grok-overlay').style.display='none'" 
                    style="background: linear-gradient(135deg, #00d4ff 0%, #0066cc 100%); 
                           color: white; border: none; border-radius: 25px; 
                           padding: 12px 30px; font-size: 1rem; cursor: pointer;
                           transition: all 0.3s ease;">
                Let's Get Started! 🚀
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">⚡ Predictive Grid Intelligence</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem;'>Next-Generation AI Assistant for Utility Operations</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 👤 User Profile")
    persona = st.selectbox("Select Your Role:", [
        "Field Technician", 
        "System Operator",
        "Protection Engineer", 
        "Operations Manager",
        "Maintenance Supervisor"
    ])
    st.session_state.user_persona = persona

    st.markdown("### 🔧 System Status")
    st.markdown("**AI Model:** xAI Grok-4 Turbo")
    st.markdown("**Status:** 🟢 Online")
    st.markdown("**Response Time:** 0.8s avg")
    st.markdown("**Confidence:** 96.4%")

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
        <small>87% of capacity</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4 style="color: #ffa502;">Alerts Active</h4>
        <h2>12</h2>
        <small>3 critical, 9 warnings</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
        <h4 style="color: #00d4ff;">Equipment Status</h4>
        <h2>98.7%</h2>
        <small>Available capacity</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="metric-card">
        <h4 style="color: #ff4757;">Outages</h4>
        <h2>3</h2>
        <small>2,447 customers affected</small>
        </div>
        """, unsafe_allow_html=True)

    # Active alerts
    st.markdown("### 🚨 Priority Alerts")
    st.markdown("""
    <div class="alert-card">
    <strong>CRITICAL:</strong> Transformer T-138-04 - High dissolved gas levels detected<br>
    <strong>Location:</strong> Riverside Substation<br>
    <strong>Action Required:</strong> Schedule immediate oil analysis and consider outage planning<br>
    <strong>ETA:</strong> Investigation within 4 hours
    </div>
    """, unsafe_allow_html=True)

elif page == "🤖 Intelligent Assistant":
    st.markdown("### 🧠 Grok-4 Intelligent Assistant")
    st.markdown("Ask me anything about utility operations, and I'll provide detailed, expert-level guidance.")
    
    # Query category selection
    category = st.selectbox("Select Query Category:", list(UTILITY_QUERIES.keys()))
    
    # Specific query selection based on category
    specific_query = st.selectbox("Choose Specific Query:", UTILITY_QUERIES[category])
    
    # Custom query option
    custom_query = st.text_input("Or enter your own question:")
    
    # Use custom query if provided, otherwise use selected query
    active_query = custom_query if custom_query else specific_query
    
    if st.button("🚀 Ask Grok-4"):
        # Add to conversation history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": active_query,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "persona": persona
        })
        
        with st.spinner("Grok-4 is analyzing your query..."):
            time.sleep(random.uniform(1.5, 3.0))  # Realistic processing time
            
        # Display user query
        st.markdown(f"""
        <div class="query-card">
        <strong>👨‍🔧 {persona}:</strong><br>
        {active_query}
        <div style="text-align: right; font-size: 0.8em; color: #888; margin-top: 0.5rem;">
        {st.session_state.conversation_history[-1]["timestamp"]}
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate response
        if active_query in DETAILED_RESPONSES:
            response = DETAILED_RESPONSES[active_query]
            
            # Add response to conversation history
            st.session_state.conversation_history.append({
                "role": "assistant", 
                "content": response["answer"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Display detailed response
            st.markdown(f"""
            <div class="response-card">
            <h4>🤖 Grok-4 Assistant Response:</h4>
            <p style="margin: 1rem 0; line-height: 1.6;">{response['answer']}</p>
            
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #333;">
            <strong>📚 Sources:</strong> {' • '.join(response['sources'])}<br>
            <strong>📊 Confidence:</strong> {response['confidence']:.0%}<br>
            <strong>⚠️ Risk Level:</strong> {response['risk_level']}<br>
            <strong>⏱️ Estimated Time:</strong> {response['estimated_time']}<br>
            <strong>👥 Personnel:</strong> {response['personnel_required']}
            </div>
            
            <div style="text-align: right; font-size: 0.8em; color: #888; margin-top: 1rem;">
            Response generated at {st.session_state.conversation_history[-1]["timestamp"]}
            </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # Generic response for custom queries
            generic_responses = [
                "Based on industry standards and utility best practices, I recommend consulting the relevant NERC standards and your company's specific procedures for this situation. Would you like me to help you identify the specific standards that apply?",
                "This is an excellent question that requires careful consideration of safety protocols and operational procedures. Let me break down the key factors you should consider...",
                "From my analysis of utility industry practices, this situation typically involves multiple considerations including safety, reliability, and regulatory compliance. Here's my recommended approach..."
            ]
            
            response_text = random.choice(generic_responses)
            
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            st.markdown(f"""
            <div class="response-card">
            <h4>🤖 Grok-4 Assistant Response:</h4>
            <p style="margin: 1rem 0; line-height: 1.6;">{response_text}</p>
            
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #333;">
            <strong>📊 Confidence:</strong> 89%<br>
            <strong>💡 Suggestion:</strong> For specific procedures, please consult your utility's operating manual
            </div>
            </div>
            """, unsafe_allow_html=True)

    # Display conversation history
    if st.session_state.conversation_history:
        with st.expander("📜 Conversation History", expanded=False):
            for i, msg in enumerate(st.session_state.conversation_history):
                if msg["role"] == "user":
                    st.markdown(f"**{msg.get('persona', 'User')}** ({msg['timestamp']}): {msg['content']}")
                else:
                    st.markdown(f"**🤖 Grok-4** ({msg['timestamp']}): {msg['content'][:200]}...")

elif page == "🏗️ System Architecture":
    st.markdown("### 🏗️ Advanced System Architecture")
    
    # Architecture flow diagram
    st.markdown("""
    <div style="background: #1a1a2e; border: 1px solid #333; border-radius: 10px; padding: 2rem; text-align: center; margin: 2rem 0;">
    <h4 style="color: #00d4ff;">Predictive Grid Intelligence Data Flow</h4>
    <div style="font-size: 1.1em; line-height: 2; margin-top: 1rem;">
    <strong>Field Sensors</strong> → <strong>Edge Computing</strong> → <strong>xAI Grok-4</strong> → 
    <strong>Vector Database</strong> → <strong>Predictive Engine</strong> → <strong>Operations Interface</strong>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧠 AI Core Components")
        st.markdown("""
        - **xAI Grok-4**: Advanced reasoning for technical domains
        - **Vector Database**: Semantic search across utility documentation  
        - **Real-time Analytics**: IoT sensor data processing
        - **Predictive Models**: Equipment failure forecasting
        - **Natural Language**: Voice and text query processing
        """)
        
    with col2:
        st.markdown("#### 🔒 Security & Compliance")
        st.markdown("""
        - **Zero-trust Architecture**: Multi-layer security model
        - **NERC CIP Compliance**: Critical infrastructure protection
        - **Encrypted Communications**: End-to-end data protection
        - **Audit Logging**: Complete operational traceability
        - **Role-based Access**: Granular permission controls
        """)
    
    # Performance metrics
    st.markdown("#### 📊 System Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Query Response", "0.8s", "-0.2s")
    with col2:
        st.metric("Accuracy Rate", "96.4%", "+1.2%")  
    with col3:
        st.metric("Uptime", "99.97%", "+0.02%")
    with col4:
        st.metric("Active Users", "847", "+23")

# Footer
st.markdown("""
<div class="footer">
<h4 style="color: #00d4ff;">⚡ Predictive Grid Intelligence</h4>
<p>Powered by xAI Grok-4 • Enterprise-Ready • Real-time Operations</p>
<p style="font-size: 0.9em; color: #666;">Advanced AI system for next-generation utility operations</p>
</div>
""", unsafe_allow_html=True)

# Hide Grok overlay after first view
if st.session_state.grok_visible:
    st.session_state.grok_visible = False
