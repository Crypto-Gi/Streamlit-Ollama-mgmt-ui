import streamlit as st

def render_sidebar():
    """Render the sidebar with navigation and configuration options"""
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; margin-bottom: 1.5rem;'>Ollama Dashboard</h2>", unsafe_allow_html=True)
        
        # Server configuration
        st.markdown("<div class='card-title'>Server Configuration</div>", unsafe_allow_html=True)
        
        # Server URL input
        server_url = st.text_input(
            "Ollama Server URL",
            value=st.session_state.server_url,
            help="Enter the base URL of your Ollama server (e.g., http://localhost:11434)"
        )
        
        # Update session state when server URL is changed
        if server_url != st.session_state.server_url:
            st.session_state.server_url = server_url
            st.session_state.api_connected = False
        
        # Test connection button
        if st.button("Test Connection", key="test_connection"):
            with st.spinner("Testing connection..."):
                from utils.api_handler import OllamaAPI
                api = OllamaAPI(st.session_state.server_url)
                success, info = api.test_connection()
                
                if success:
                    st.session_state.api_connected = True
                    st.session_state.server_info = info
                    st.success("Connected successfully!")
                else:
                    st.session_state.api_connected = False
                    st.error(f"Connection failed: {info.get('error', 'Unknown error')}")
        
        # Display connection status
        if st.session_state.api_connected:
            st.markdown(
                "<div><span class='status-indicator success'></span><span class='status-text'>Connected</span></div>",
                unsafe_allow_html=True
            )
            version = st.session_state.server_info.get("version", "Unknown")
            st.markdown(f"<div class='card-subtitle'>Server version: {version}</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div><span class='status-indicator error'></span><span class='status-text'>Disconnected</span></div>",
                unsafe_allow_html=True
            )
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("<div class='card-title'>Navigation</div>", unsafe_allow_html=True)
        
        # Navigation items
        nav_items = {
            "Overview": "🏠",
            "Model Management": "📦",
            "Model Interaction": "💬",
            "Server Status": "📊"
        }
        
        # Create clickable navigation items
        for name, icon in nav_items.items():
            active_class = "active" if st.session_state.current_page == name else ""
            
            # Use buttons instead of markdown for navigation
            if st.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
                st.session_state.current_page = name
                st.rerun()
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # Theme toggle
        st.markdown("<div class='card-title'>Appearance</div>", unsafe_allow_html=True)
        
        # Dark mode toggle (currently for illustration only since we're using custom CSS)
        dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        # Footer
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown(
            "<div style='position: fixed; bottom: 0; padding: 1rem; width: 100%;'>"
            "<p style='text-align: center; font-size: 0.8rem; color: #8a8a8e;'>"
            "Built with Streamlit ❤️<br/>Apple-inspired UI</p></div>",
            unsafe_allow_html=True
        )
