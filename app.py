import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd

# Import components and utilities
from utils.api_handler import OllamaAPI
from utils.styling import apply_custom_styling
from components.sidebar import render_sidebar
from components.model_management import render_model_management
from components.model_interaction import render_model_interaction
from components.server_status import render_server_status
from components.overview import render_overview

# Page configuration
st.set_page_config(
    page_title="Ollama Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
apply_custom_styling()

# Initialize session state if not exists
if "server_url" not in st.session_state:
    st.session_state.server_url = "http://localhost:11434"
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"
if "models_data" not in st.session_state:
    st.session_state.models_data = []
if "server_info" not in st.session_state:
    st.session_state.server_info = {}
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

# Custom CSS to style the app
st.markdown("""
<style>
    /* Light/Dark mode */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Rest of your existing CSS */
    .card {
        background-color: var(--card-background);
    }
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: var(--background-color);
        color: var(--text-color);
    }
</style>
""", unsafe_allow_html=True)

# Main App Layout
def main():
    # Initialize API handler
    api = OllamaAPI(st.session_state.server_url)
    
    # Render sidebar with connection settings
    render_sidebar()
    
    # Header with gradient
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-text">Ollama Dashboard</h1>
            <p class="subheader-text">Elegant model management for LLMs</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display current page based on navigation selection
    if st.session_state.current_page == "Overview":
        render_overview(api)
    elif st.session_state.current_page == "Model Management":
        render_model_management(api)
    elif st.session_state.current_page == "Model Interaction":
        render_model_interaction(api)
    elif st.session_state.current_page == "Server Status":
        render_server_status(api)
    
    # Add custom footer in a non-obtrusive position
    st.markdown("""
    <div class='custom-footer'>
        Built with Streamlit ❤️<br>Apple-inspired UI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
