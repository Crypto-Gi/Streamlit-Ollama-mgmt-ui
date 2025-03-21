import streamlit as st
import pandas as pd
import time
from datetime import datetime

def render_server_status(api):
    """Render the server status dashboard with real-time server information"""
    
    st.markdown("<div class='card-title'>Server Status</div>", unsafe_allow_html=True)
    
    # Check if API is connected first
    if not st.session_state.get("api_connected", False):
        st.warning("Not connected to Ollama server. Please configure and test your connection in the sidebar.")
        
        # Display example connection instructions
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Connection Required</div>
                <div class="card-subtitle">
                    You need to connect to an Ollama server to view server status.
                    Please configure and test your connection in the sidebar.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Show troubleshooting tips even when disconnected
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Troubleshooting</div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="card">
                <div class="card-subtitle">
                    <strong>Common Solutions:</strong>
                    <ul>
                        <li>Make sure Ollama is running with <code>ollama serve</code></li>
                        <li>Check that the server URL is correct (default: http://localhost:11434)</li>
                        <li>Ensure port 11434 is accessible and not blocked by firewall</li>
                        <li>Check if Ollama is running on a different port</li>
                    </ul>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        return
    
    # Create two columns for server info and loaded models
    col1, col2 = st.columns(2)
    
    with col1:
        # Server Information Card
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Server Information</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Get server version info
        with st.spinner("Fetching server information..."):
            server_info = api.get_version()
        
        if "error" not in server_info:
            # Display server metrics
            st.metric("Version", server_info.get('version', 'Unknown'))
            st.metric("Build", server_info.get('build', 'Unknown'))
            
            # Server status indicator
            st.markdown(
                """
                <div style="margin-top: 1rem;">
                    <span class="status-indicator success"></span>
                    <span class="status-text">Server Online</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Server URL
            st.markdown(
                f"""
                <div class="card-subtitle" style="margin-top: 1rem;">
                    <strong>Server URL:</strong> {st.session_state.server_url}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.error(f"Could not fetch server information: {server_info.get('error')}")
            
            # Server status indicator - error
            st.markdown(
                """
                <div style="margin-top: 1rem;">
                    <span class="status-indicator error"></span>
                    <span class="status-text">Server Offline</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    with col2:
        # Models Status Card
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Model Status</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Get current models
        with st.spinner("Fetching models..."):
            models = api.list_models()
            st.session_state.models_data = models
        
        # Display model stats
        if models:
            total_size_bytes = sum(model.get("size", 0) for model in models)
            
            # Calculate size in appropriate units
            if total_size_bytes > 1024 * 1024 * 1024:
                total_size_str = f"{total_size_bytes / (1024 * 1024 * 1024):.2f} GB"
            elif total_size_bytes > 1024 * 1024:
                total_size_str = f"{total_size_bytes / (1024 * 1024):.2f} MB"
            else:
                total_size_str = f"{total_size_bytes / 1024:.2f} KB"
            
            st.metric("Total Models", len(models))
            st.metric("Total Size", total_size_str)
            
            # Latest model
            newest_model = None
            newest_date = None
            
            for model in models:
                model_date = model.get("modified_at", "")
                if model_date and (newest_date is None or model_date > newest_date):
                    newest_date = model_date
                    newest_model = model.get("name", "Unknown")
            
            if newest_model:
                st.metric("Latest Model", newest_model)
        else:
            st.warning("No models found on server")
    
    # Refresh button for real-time updates
    if st.button("Refresh Status", key="refresh_status"):
        st.rerun()
    
    # Server Health Monitoring
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Server Health</div>", unsafe_allow_html=True)
    
    # Create health monitoring metrics (sample data, in a real app this would be from actual monitoring)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">API Response Time</div>
                <div style="font-size: 2rem; font-weight: 700; text-align: center;">
                    <span style="color: #30d158;">42 ms</span>
                </div>
                <div class="card-subtitle" style="text-align: center;">
                    Healthy
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">VRAM Usage</div>
                <div style="font-size: 2rem; font-weight: 700; text-align: center;">
                    <span style="color: #ff9f0a;">67%</span>
                </div>
                <div class="card-subtitle" style="text-align: center;">
                    Moderate
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Disk Space</div>
                <div style="font-size: 2rem; font-weight: 700; text-align: center;">
                    <span style="color: #30d158;">32%</span>
                </div>
                <div class="card-subtitle" style="text-align: center;">
                    Available
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Server actions
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Server Management</div>", unsafe_allow_html=True)
    
    # Server management actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Server Actions</div>
                <div class="card-subtitle">
                    Administrative actions for the Ollama server.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Actions (Note: These would need actual implementations depending on server setup)
        st.button("Test API Connection", key="test_api_btn")
        st.button("Clear Cache", key="clear_cache_btn", disabled=True)
        st.button("Check for Updates", key="check_updates_btn", disabled=True)
    
    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Troubleshooting</div>
                <div class="card-subtitle">
                    Helpful resources for troubleshooting server issues.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Troubleshooting tips
        st.markdown(
            """
            * Make sure Ollama is running with `ollama serve`
            * Check that the server URL is correct
            * Ensure port 11434 is accessible
            * View Ollama logs for detailed information
            """
        )
    
    # Last updated timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(
        f"""
        <div style="text-align: center; color: #8a8a8e; margin-top: 2rem; font-size: 0.8rem;">
            Last updated: {current_time}
        </div>
        """, 
        unsafe_allow_html=True
    )
