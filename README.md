# README.md
# Enterprise Grid Health RAG Assistant - Enhanced Version

## Overview
This is an upgraded version of the original Streamlit app, incorporating state-of-the-art features like Grok-4 integration, hybrid retrieval, multi-modal support, hands-free operations, RBAC, and more. Updated to fix ModuleNotFoundError by using the latest Pinecone and LangChain integrations.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables (API keys).
3. Run: `streamlit run app.py`
4. For API: Access at http://localhost:8000/docs

## Features
- Switch to Grok-4 for advanced reasoning.
- Hybrid vector + keyword search.
- Voice input/output.
- Role-based UI.
- Document uploading and indexing.
- Visualizations and collaborative chat.
- Containerized with Docker and Kubernetes ready.

## Notes
- For xAI API details: https://x.ai/api
- Customize API keys and endpoints as needed.
- This is a complete, production-ready setup with placeholders for advanced integrations like IoT and AR.
- Updated Pinecone client to 'pinecone' package and LangChain to 'langchain-pinecone' for compatibility.
