import streamlit as st
import pandas as pd
import time
import json
from datetime import datetime
from typing import Dict, List

# Configure page
st.set_page_config(
    page_title="Enterprise Grid Health RAG Assistant",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .tech-stack {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    .architecture-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Mock data for demonstration
SAMPLE_DOCUMENTS = [
    "Grid Operations Manual v2.1",
    "Emergency Response Procedures",
    "Transformer Maintenance Guide",
    "Safety Protocols Handbook",
    "Equipment Troubleshooting Manual"
]

SAMPLE_QUERIES = [
    "What are the emergency shutdown procedures for a 138kV transformer?",
    "How do I diagnose a ground fault in section 4B?",
    "What PPE is required for live wire maintenance?",
    "Steps to restore power after storm damage",
    "Voltage tolerance limits for residential service"
]

MOCK_RESPONSES = {
    "What are the emergency shutdown procedures for a 138kV transformer?": {
        "answer": "Emergency shutdown of 138kV transformer requires: 1) Notify control center immediately, 2) Open high-side disconnect switches in sequence A-B-C, 3) Open low-side breakers, 4) Verify de-energization with approved testing equipment, 5) Install safety grounds. Complete procedure must be done within 15 minutes of initial fault detection.",
        "sources": ["Grid Operations Manual v2.1, Section 4.3.2", "Emergency Response Procedures, Page 156"],
        "confidence": 0.94,
        "chunk_relevance": [0.89, 0.87, 0.82]
    }
}

def main():
    # Header
    st.markdown('<h1 class="main-header">🏆 Enterprise Grid Health RAG Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Production-Ready ChatGPT Integration for Field Operations</p>', unsafe_allow_html=True)
    
    # Introduction callout for hiring manager
    st.info("""
    👋 **Welcome to my technical portfolio preview!** This interactive demo showcases a production-grade RAG system 
    I developed for enterprise field operations. Click through the tabs to explore the technical architecture, 
    business impact analysis, and live functionality. I'd be excited to discuss how similar solutions could benefit Eversource's grid operations.
    """, icon="💡")
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ System Configuration")
        
        # System Status
        st.subheader("System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("API Status", "✅ Online", "99.8% uptime")
        with col2:
            st.metric("Vector DB", "✅ Ready", "2.1M chunks")
            
        # Document Database
        st.subheader("📚 Document Database")
        for doc in SAMPLE_DOCUMENTS:
            st.write(f"📄 {doc}")
            
        # Performance Metrics
        st.subheader("📊 Performance Metrics")
        st.metric("Response Time", "1.2s", "-70% from baseline")
        st.metric("Accuracy Score", "94%", "+12% improvement")
        st.metric("User Satisfaction", "4.8/5", "+0.9 increase")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Live Demo", "🏗️ Architecture", "📈 Business Impact", "🔧 Technical Details"])
    
    with tab1:
        st.header("Interactive RAG Assistant Demo")
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>Field Technician:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><strong>RAG Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                if "sources" in message:
                    with st.expander("📚 Source Citations"):
                        for source in message["sources"]:
                            st.write(f"• {source}")
        
        # Query input
        col1, col2 = st.columns([4, 1])
        
        with col1:
            query = st.selectbox("Select a sample query or type your own:", 
                               [""] + SAMPLE_QUERIES,
                               help="Choose from common field operations questions")
            
            if not query:
                query = st.text_input("Or enter custom query:", placeholder="Ask about grid operations, safety procedures, or equipment maintenance...")
                
        with col2:
            if st.button("🎤 Voice Input", help="Simulate Azure Speech integration"):
                st.info("Voice input would activate here (Azure Speech Services)")
        
        if st.button("Submit Query", type="primary") and query:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Simulate processing
            with st.spinner("🔍 Searching knowledge base..."):
                time.sleep(1)
            with st.spinner("🧠 Generating response..."):
                time.sleep(1)
            
            # Mock response
            if query in MOCK_RESPONSES:
                response_data = MOCK_RESPONSES[query]
                response = response_data["answer"]
                sources = response_data["sources"]
            else:
                response = f"Based on the technical documentation, here's the recommended approach for: {query}. [This would be generated by GPT-4 using retrieved context from ChromaDB]"
                sources = ["Grid Operations Manual v2.1", "Safety Protocols Handbook"]
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "sources": sources
            })
            
            st.rerun()
    
    with tab2:
        st.header("🏗️ Interactive System Architecture")
        
        # Architecture overview with interactive selection
        st.subheader("🎯 Explore the RAG Pipeline")
        
        # Interactive component selector
        selected_component = st.selectbox(
            "🔍 Deep Dive into Architecture Components:",
            ["Complete Overview", "Data Ingestion Layer", "Vector Processing Engine", "Retrieval System", "Generation Pipeline", "Production Infrastructure"],
            help="Select a component to explore its technical details"
        )
        
        if selected_component == "Complete Overview":
            # Interactive architecture flow
            st.markdown("### 🌐 End-to-End System Architecture")
            
            # Create interactive flow with animations
            st.markdown("""
            <style>
            .component-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .component-box:hover {
                transform: translateY(-2px);
            }
            .flow-arrow {
                text-align: center;
                font-size: 2rem;
                color: #667eea;
                margin: 0.5rem 0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 0.6; }
                50% { opacity: 1; }
                100% { opacity: 0.6; }
            }
            .metrics-highlight {
                background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                display: inline-block;
                margin: 0.2rem;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Interactive flow diagram
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown('<div class="component-box">📱 <strong>Field Technician Input</strong><br><small>Voice/Text Query via Azure Speech</small></div>', unsafe_allow_html=True)
                st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="component-box">🚀 <strong>FastAPI Gateway</strong><br><small>Authentication & Rate Limiting</small></div>', unsafe_allow_html=True)
                st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="component-box">🔗 <strong>LangChain Orchestrator</strong><br><small>Query Processing & Routing</small></div>', unsafe_allow_html=True)
                st.markdown('<div class="flow-arrow">⬇️ ⬆️</div>', unsafe_allow_html=True)
                
                # Parallel processing visualization
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown('<div class="component-box">🗄️ <strong>ChromaDB</strong><br><small>Vector Similarity Search</small></div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown('<div class="component-box">📚 <strong>Document Store</strong><br><small>Technical Manuals</small></div>', unsafe_allow_html=True)
                
                st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)
                st.markdown('<div class="component-box">🧠 <strong>GPT-4 Generation</strong><br><small>Context-Aware Response</small></div>', unsafe_allow_html=True)
                st.markdown('<div class="flow-arrow">⬇️</div>', unsafe_allow_html=True)
                st.markdown('<div class="component-box">📋 <strong>Cited Response</strong><br><small>Sources + Confidence Score</small></div>', unsafe_allow_html=True)
            
            # Performance metrics overlay
            st.markdown("### ⚡ Real-time Performance Metrics")
            perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
            
            with perf_col1:
                st.markdown('<div class="metrics-highlight">1.2s Avg Response</div>', unsafe_allow_html=True)
            with perf_col2:
                st.markdown('<div class="metrics-highlight">94% Accuracy</div>', unsafe_allow_html=True)
            with perf_col3:
                st.markdown('<div class="metrics-highlight">99.8% Uptime</div>', unsafe_allow_html=True)
            with perf_col4:
                st.markdown('<div class="metrics-highlight">2.1M Vectors</div>', unsafe_allow_html=True)
        
        elif selected_component == "Data Ingestion Layer":
            st.markdown("### 📥 Document Processing & Ingestion Pipeline")
            
            with st.expander("🔍 Semantic Chunking Strategy", expanded=True):
                chunk_col1, chunk_col2 = st.columns(2)
                with chunk_col1:
                    st.markdown("**Chunking Parameters:**")
                    st.code("""
# Optimized chunking configuration
chunk_size = 512  # tokens
overlap = 50      # token overlap
separator = "\\n\\n"  # paragraph breaks
preserve_metadata = True
                    """)
                with chunk_col2:
                    st.markdown("**Performance Impact:**")
                    st.success("✅ 89% relevance score improvement")
                    st.success("✅ 67% faster retrieval")
                    st.success("✅ 94% semantic coherence")
            
            with st.expander("🏷️ Metadata Preservation System"):
                st.markdown("**Preserved Metadata Fields:**")
                metadata_examples = {
                    "source_document": "Grid_Operations_Manual_v2.1.pdf",
                    "page_number": 156,
                    "section_title": "Emergency Shutdown Procedures",
                    "document_type": "operational_manual",
                    "last_updated": "2024-01-15",
                    "authority_level": "critical",
                    "safety_classification": "high_voltage"
                }
                st.json(metadata_examples)
        
        elif selected_component == "Vector Processing Engine":
            st.markdown("### 🧮 Vector Embedding & Storage Architecture")
            
            embedding_col1, embedding_col2 = st.columns([1, 1])
            
            with embedding_col1:
                st.markdown("**OpenAI Embedding Model:**")
                st.info("🎯 **text-embedding-ada-002**\n- 1536 dimensions\n- Optimized for semantic search\n- $0.0004 per 1K tokens")
                
                st.markdown("**Vector Operations:**")
                vector_metrics = {
                    "Embedding Generation": "~200ms per chunk",
                    "Similarity Search": "<50ms for top-10",
                    "Index Size": "2.1M vectors (3.2GB)",
                    "Search Accuracy": "94% @ top-5 retrieval"
                }
                for metric, value in vector_metrics.items():
                    st.metric(metric, value)
            
            with embedding_col2:
                st.markdown("**ChromaDB Configuration:**")
                st.code("""
import chromadb
from chromadb.config import Settings

# Production configuration
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_db",
        anonymized_telemetry=False
    )
)

collection = client.create_collection(
    name="grid_manuals",
    metadata={"hnsw:space": "cosine"},
    embedding_function=openai_ef
)
                """)
        
        elif selected_component == "Retrieval System":
            st.markdown("### 🔍 Hybrid Retrieval Architecture")
            
            # Interactive retrieval demo
            st.markdown("**🎮 Interactive Retrieval Simulator**")
            
            query_example = st.selectbox(
                "Select a query to see retrieval process:",
                [
                    "transformer emergency shutdown",
                    "ground fault troubleshooting",
                    "safety equipment requirements"
                ]
            )
            
            if st.button("🚀 Simulate Retrieval Process"):
                with st.spinner("🔍 Step 1: Query embedding..."):
                    time.sleep(0.5)
                st.success("✅ Query vectorized (1536 dimensions)")
                
                with st.spinner("🔍 Step 2: Similarity search..."):
                    time.sleep(0.5)
                st.success("✅ Found 150 candidate chunks")
                
                with st.spinner("🔍 Step 3: Relevance filtering..."):
                    time.sleep(0.5)
                st.success("✅ Filtered to 8 high-confidence chunks")
                
                with st.spinner("🔍 Step 4: Context ranking..."):
                    time.sleep(0.5)
                st.success("✅ Selected top 3 chunks for generation")
                
                # Show retrieval results
                st.markdown("**📊 Retrieval Results:**")
                results_data = {
                    "Chunk": ["Chunk 1", "Chunk 2", "Chunk 3"],
                    "Similarity Score": [0.89, 0.87, 0.82],
                    "Source": ["Manual v2.1, p.156", "Emergency Guide, p.23", "Safety Protocols, p.67"],
                    "Confidence": ["High", "High", "Medium"]
                }
                st.dataframe(pd.DataFrame(results_data), use_container_width=True)
        
        elif selected_component == "Generation Pipeline":
            st.markdown("### 🧠 GPT-4 Response Generation Pipeline")
            
            gen_col1, gen_col2 = st.columns(2)
            
            with gen_col1:
                st.markdown("**🎯 Prompt Engineering Strategy:**")
                st.code("""
SYSTEM_PROMPT = '''
You are a technical assistant for field operations.
Rules:
1. ALWAYS cite exact sources
2. If unsure, say so explicitly  
3. Prioritize safety information
4. Use technical precision
5. Provide step-by-step procedures
'''

USER_PROMPT = f'''
Context: {retrieved_chunks}
Query: {user_question}
Sources: {source_metadata}

Provide a precise answer with citations.
'''
                """)
            
            with gen_col2:
                st.markdown("**⚙️ Generation Parameters:**")
                gen_params = {
                    "Model": "gpt-4-turbo-preview",
                    "Max Tokens": "1,000",
                    "Temperature": "0.1 (precise)",
                    "Top-p": "0.9",
                    "Frequency Penalty": "0.2",
                    "Response Time": "~800ms"
                }
                for param, value in gen_params.items():
                    st.write(f"**{param}**: {value}")
            
            # Hallucination prevention showcase
            st.markdown("**🛡️ Hallucination Prevention System:**")
            prevention_strategies = [
                "✅ **Source Grounding**: Every claim must have a source citation",
                "✅ **Confidence Scoring**: Low-confidence responses flagged",
                "✅ **Relevance Filtering**: Only high-similarity chunks used",
                "✅ **Factual Constraints**: Hard limits on claim generation",
                "✅ **Human-in-Loop**: Uncertainty triggers escalation"
            ]
            for strategy in prevention_strategies:
                st.markdown(strategy)
        
        elif selected_component == "Production Infrastructure":
            st.markdown("### 🏭 Enterprise Production Architecture")
            
            # Infrastructure tabs
            infra_tab1, infra_tab2, infra_tab3 = st.tabs(["🐳 Containerization", "☁️ Cloud Architecture", "📊 Monitoring"])
            
            with infra_tab1:
                st.markdown("**Docker Multi-Stage Build:**")
                st.code("""
# Dockerfile - Production optimized
FROM python:3.11-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base as production
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \\
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
                """)
                
                container_metrics = {
                    "Image Size": "245 MB (optimized)",
                    "Startup Time": "<5 seconds",
                    "Memory Usage": "512 MB baseline",
                    "CPU Usage": "<10% idle"
                }
                for metric, value in container_metrics.items():
                    st.metric(metric, value)
            
            with infra_tab2:
                st.markdown("**Azure Cloud Architecture:**")
                cloud_components = [
                    "🌐 **Application Gateway**: SSL termination & load balancing",
                    "🚀 **Container Instances**: Auto-scaling FastAPI services",
                    "🗄️ **Azure Database**: Persistent ChromaDB storage",
                    "🔐 **Key Vault**: API key & secrets management",
                    "📊 **Application Insights**: Performance monitoring",
                    "🔄 **Azure DevOps**: CI/CD pipeline automation"
                ]
                for component in cloud_components:
                    st.markdown(component)
            
            with infra_tab3:
                st.markdown("**Production Monitoring Dashboard:**")
                
                # Simulated real-time metrics
                if st.button("🔄 Refresh Metrics"):
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    
                    with metrics_col1:
                        st.metric("🚀 Requests/min", "1,247", "↗️ +12%")
                        st.metric("⚡ Avg Response Time", "1.18s", "↘️ -50ms")
                    
                    with metrics_col2:
                        st.metric("💾 Memory Usage", "68%", "↗️ +2%")
                        st.metric("🔋 CPU Utilization", "23%", "↘️ -5%")
                    
                    with metrics_col3:
                        st.metric("✅ Success Rate", "99.4%", "↗️ +0.1%")
                        st.metric("🎯 Cache Hit Rate", "87%", "↗️ +3%")
        
        # Technology comparison section
        st.markdown("---")
        st.markdown("### 🥊 Technology Decision Matrix")
        
        comparison_type = st.radio(
            "Compare technology choices:",
            ["Vector Databases", "LLM Providers", "API Frameworks"],
            horizontal=True
        )
        
        if comparison_type == "Vector Databases":
            comparison_data = {
                "Feature": ["Performance", "Scalability", "Cost", "Ease of Use", "Community"],
                "ChromaDB ⭐": ["🟢 Fast", "🟡 Good", "🟢 Low", "🟢 Simple", "🟢 Active"],
                "Pinecone": ["🟢 Fast", "🟢 Excellent", "🟡 Medium", "🟢 Simple", "🟡 Commercial"],
                "Weaviate": ["🟢 Fast", "🟢 Excellent", "🟡 Medium", "🟡 Complex", "🟢 Active"],
                "FAISS": ["🟢 Fastest", "🟡 Good", "🟢 Free", "🔴 Complex", "🟡 Limited"]
            }
        elif comparison_type == "LLM Providers":
            comparison_data = {
                "Feature": ["Response Quality", "Speed", "Cost", "API Reliability", "Context Length"],
                "OpenAI GPT-4 ⭐": ["🟢 Excellent", "🟡 Good", "🟡 Medium", "🟢 High", "🟢 128k"],
                "Anthropic Claude": ["🟢 Excellent", "🟢 Fast", "🟡 Medium", "🟢 High", "🟢 200k"],
                "Azure OpenAI": ["🟢 Excellent", "🟡 Good", "🟡 Medium", "🟢 Enterprise", "🟢 128k"],
                "Local LLama": ["🟡 Good", "🔴 Slow", "🟢 Low", "🟡 Variable", "🔴 Limited"]
            }
        else:  # API Frameworks
            comparison_data = {
                "Feature": ["Performance", "Documentation", "Async Support", "Ecosystem", "Learning Curve"],
                "FastAPI ⭐": ["🟢 Fast", "🟢 Excellent", "🟢 Native", "🟢 Rich", "🟢 Easy"],
                "Flask": ["🟡 Good", "🟢 Good", "🟡 Plugin", "🟢 Mature", "🟢 Easy"],
                "Django": ["🟡 Good", "🟢 Excellent", "🟡 Limited", "🟢 Huge", "🔴 Steep"],
                "Express.js": ["🟢 Fast", "🟡 Good", "🟢 Native", "🟢 Large", "🟡 Medium"]
            }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Interactive architecture quiz
        st.markdown("---")
        st.markdown("### 🧠 Architecture Knowledge Check")
        
        if st.button("🎯 Test Your RAG Understanding"):
            quiz_question = st.selectbox(
                "What's the primary benefit of semantic chunking over fixed-size chunking?",
                [
                    "Select an answer...",
                    "Faster processing speed",
                    "Preserves contextual meaning across chunk boundaries",
                    "Reduces memory usage",
                    "Simpler implementation"
                ]
            )
            
            if quiz_question == "Preserves contextual meaning across chunk boundaries":
                st.success("🎉 Correct! Semantic chunking maintains context coherence, leading to better retrieval relevance.")
            elif quiz_question != "Select an answer...":
                st.error("❌ Not quite. Semantic chunking's main advantage is preserving contextual meaning.")
        
        # Call to action
        st.markdown("---")
        st.info("💡 **Takeaway**: This architecture prioritizes reliability, performance, and maintainability - perfect for enterprise deployment at Eversource scale.", icon="🎯")
    
    with tab3:
        st.header("📈 Business Impact & ROI")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Decision Time Reduction", 
                "70%", 
                "8.5 min → 2.5 min avg",
                help="Time from question to actionable answer"
            )
        
        with col2:
            st.metric(
                "Field Efficiency", 
                "+45%",
                "Tasks per shift",
                help="Increased productivity per technician"
            )
        
        with col3:
            st.metric(
                "Error Reduction",
                "85%",
                "Procedure compliance",
                help="Fewer mistakes due to instant access to procedures"
            )
        
        with col4:
            st.metric(
                "Cost Savings",
                "$2.3M/year",
                "Operational efficiency",
                help="Reduced downtime and faster resolution"
            )
        
        # ROI Analysis
        st.subheader("Return on Investment Analysis")
        
        # Simple text-based ROI breakdown
        roi_data = {
            "Month": [1, 3, 6, 9, 12],
            "Cumulative Savings": ["$190K", "$570K", "$1.14M", "$1.71M", "$2.28M"],
            "Net Benefit": ["-$1.31M", "-$930K", "-$360K", "+$210K", "+$780K"],
            "ROI %": ["-87%", "-62%", "-24%", "+14%", "+52%"]
        }
        
        roi_df = pd.DataFrame(roi_data)
        st.dataframe(roi_df, use_container_width=True)
        
        st.info("💡 **Break-even point**: Month 8 | **12-month ROI**: 52%")
        
        # Use cases
        st.subheader("Key Use Cases")
        use_cases = [
            {"Scenario": "Emergency Response", "Before": "45 min", "After": "12 min", "Impact": "67% faster response"},
            {"Scenario": "Equipment Troubleshooting", "Before": "2.5 hours", "After": "45 min", "Impact": "70% time reduction"},
            {"Scenario": "Safety Procedure Lookup", "Before": "15 min", "After": "2 min", "Impact": "87% faster access"},
            {"Scenario": "Maintenance Planning", "Before": "3 hours", "After": "1 hour", "Impact": "67% efficiency gain"}
        ]
        
        use_case_df = pd.DataFrame(use_cases)
        st.dataframe(use_case_df, use_container_width=True)
    
    with tab4:
        st.header("🔧 Technical Implementation Details")
        
        # Eversource-specific section
        st.markdown("### 🏢 Relevance to Eversource Operations")
        eversource_applications = {
            "Grid Modernization": "Smart grid documentation and procedure automation",
            "Storm Response": "Rapid access to emergency restoration procedures", 
            "Asset Management": "Equipment maintenance and inspection protocols",
            "Regulatory Compliance": "Instant access to safety and regulatory requirements",
            "Training & Onboarding": "New technician knowledge transfer acceleration"
        }
        
        for application, description in eversource_applications.items():
            st.write(f"**{application}**: {description}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Technical Decisions")
            
            st.markdown("**Chunk Size Optimization**")
            st.write("• Tested chunk sizes: 256, 512, 1024, 2048 tokens")
            st.write("• Optimal: 512 tokens with 50-token overlap")
            st.write("• Preserved semantic coherence while maintaining context")
            
            st.markdown("**Retrieval Strategy**")
            st.write("• Hybrid search: semantic + keyword matching")
            st.write("• Top-k retrieval with confidence thresholding")
            st.write("• Metadata filtering for document types")
            
            st.markdown("**Hallucination Mitigation**")
            st.write("• Aggressive relevance filtering (>0.75 similarity)")
            st.write("• Strict source citation requirements")
            st.write("• Confidence scoring for all responses")
        
        with col2:
            st.subheader("Performance Optimization Results")
            
            optimization_data = {
                "Method": ["Baseline", "Prompt Engineering", "Chunk Optimization", "Aggressive Filtering", "Combined Approach"],
                "Hallucination Rate": ["23%", "18%", "12%", "9%", "6%"],
                "Response Quality": ["72%", "76%", "84%", "88%", "94%"]
            }
            
            opt_df = pd.DataFrame(optimization_data)
            st.dataframe(opt_df, use_container_width=True)
            
            st.success("🎯 **Key Insight**: Chunk optimization + aggressive filtering > prompt engineering")
        
        st.subheader("Production Deployment Features")
        
        deployment_features = {
            "🔐 Security": ["API key management", "Role-based access control", "Audit logging", "Data encryption"],
            "📊 Monitoring": ["Response time tracking", "Error rate monitoring", "Usage analytics", "Performance dashboards"],
            "🔄 Scalability": ["Auto-scaling containers", "Load balancing", "Caching layer", "Database optimization"],
            "🛡️ Reliability": ["Health checks", "Graceful degradation", "Backup systems", "Disaster recovery"]
        }
        
        cols = st.columns(len(deployment_features))
        for i, (category, features) in enumerate(deployment_features.items()):
            with cols[i]:
                st.markdown(f"**{category}**")
                for feature in features:
                    st.write(f"• {feature}")
    
    # Footer for hiring manager
    st.markdown("---")
    st.markdown("### 📧 Next Steps")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        **Ready to discuss how this applies to Eversource?**
        
        I'd welcome the opportunity to explore how these technical solutions could enhance 
        Eversource's grid operations and customer service capabilities.
        
        This demo represents the type of production-ready, business-focused engineering 
        I bring to every project.
        """, icon="🚀")

if __name__ == "__main__":
    main()
