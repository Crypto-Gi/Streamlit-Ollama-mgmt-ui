import streamlit as st
import time
import datetime
from dateutil import parser
import pandas as pd
import plotly.express as px

def render_overview(api):
    """Render the overview dashboard with model summary cards"""
    
    st.markdown("<div class='card-title'>Models Overview</div>", unsafe_allow_html=True)
    
    # Check if API is connected first
    if not st.session_state.get("api_connected", False):
        st.warning("Not connected to Ollama server. Please configure and test your connection in the sidebar.")
        
        # Display example connection instructions
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Connection Instructions</div>
                <div class="card-subtitle">
                    1. Ensure your Ollama server is running
                    2. Enter the correct server URL in the sidebar (default: http://localhost:11434)
                    3. Click "Test Connection" to verify
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
        
    # Running Models Section
    st.markdown("<div class='card-title'>Currently Running Models</div>", unsafe_allow_html=True)
    
    # Display running models
    running_models = api.get_running_models()
    
    if not running_models:
        st.info("No models are currently running in memory.")
    else:
        # Create table columns
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 2, 2])
        
        with col1:
            st.markdown("<div class='table-header'>Model Name</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='table-header'>VRAM Usage</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='table-header'>Family</div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='table-header'>Expiration</div>", unsafe_allow_html=True)
        with col5:
            st.markdown("<div class='table-header'>Unload</div>", unsafe_allow_html=True)
        
        st.markdown("<hr/>", unsafe_allow_html=True)
        
        # Add each running model to the table
        for model in running_models:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 2, 2])
            
            # Convert size to GB
            size_gb = model.get("size_vram", 0) / (1024 * 1024 * 1024)
            size_gb_rounded = round(size_gb, 2)
            
            # Calculate time remaining until expiration
            expires_at = model.get("expires_at", "")
            if expires_at:
                try:
                    # Parse the expiration time
                    expiration_time = parser.parse(expires_at)
                    current_time = datetime.datetime.now(datetime.timezone.utc)
                    
                    # Calculate time difference
                    if expiration_time > current_time:
                        time_diff = expiration_time - current_time
                        
                        # Format time remaining in HH:MM:SS format
                        days = time_diff.days
                        hours, remainder = divmod(time_diff.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        
                        # Format based on time remaining
                        if days > 0:
                            time_remaining = f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
                            time_color = "green"
                        else:
                            time_remaining = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                            time_color = "green" if hours > 1 else ("orange" if minutes > 15 else "red")
                            
                        expiration_display = f"<span style='color: {time_color}'>{time_remaining}</span>"
                    else:
                        expiration_display = "<span style='color: red'>Expired</span>"
                except Exception as e:
                    expiration_display = "<span style='color: grey'>Error parsing time</span>"
            else:
                expiration_display = "<span style='color: grey'>Unknown</span>"
                
            # Get family information
            family = model.get("details", {}).get("family", "Unknown")
            
            with col1:
                st.markdown(f"<div class='table-cell'>{model.get('name', 'Unknown')}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='table-cell'>{size_gb_rounded} GB</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='table-cell'>{family}</div>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<div class='table-cell'>{expiration_display}</div>", unsafe_allow_html=True)
            with col5:
                # Add unload button for each model
                if st.button(f"Unload", key=f"unload_{model.get('name', 'Unknown')}", use_container_width=True):
                    with st.spinner(f"Unloading {model.get('name', 'Unknown')}..."):
                        try:
                            # Use the correct method from the API handler to unload the model
                            response = api.remove_model_from_vram(model.get('name', 'Unknown'))
                            if response and "error" not in response:
                                st.success(f"Model {model.get('name', 'Unknown')} unloaded successfully")
                                time.sleep(1)  # Give a moment for the message to show
                                st.rerun()  # Refresh the page
                            else:
                                error_msg = response.get("error", "Unknown error") if response else "No response from API"
                                st.error(f"Error: {error_msg}")
                        except Exception as e:
                            st.error(f"Error unloading model: {str(e)}")
                
    # Auto-refresh button and timer
    col1, col2 = st.columns([3, 1])
    
    # Initialize last_refresh if not already in session state
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.datetime.now()
    
    with col1:
        # Show the last refresh time
        time_since_refresh = (datetime.datetime.now() - st.session_state.last_refresh).total_seconds()
        st.markdown(f"<div style='color: gray; font-size: 0.8em;'>Last updated: {time_since_refresh:.1f} seconds ago</div>", unsafe_allow_html=True)
    
    with col2:
        if st.button("Refresh Data", key="refresh_running_models"):
            st.session_state.last_refresh = datetime.datetime.now()
            st.rerun()
    
    # Set up auto-refresh (every 5 seconds)
    if "last_auto_refresh" not in st.session_state:
        st.session_state.last_auto_refresh = datetime.datetime.now()
    
    # Check if 5 seconds have passed since last auto-refresh
    auto_refresh_interval = 5  # seconds
    time_since_auto_refresh = (datetime.datetime.now() - st.session_state.last_auto_refresh).total_seconds()
    
    if time_since_auto_refresh >= auto_refresh_interval:
        st.session_state.last_auto_refresh = datetime.datetime.now()
        st.session_state.last_refresh = datetime.datetime.now()
        st.rerun()
        
    # Refresh models data
    with st.spinner("Loading models..."):
        try:
            models = api.list_models()
            st.session_state.models_data = models
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            models = []
    
    # Display models summary
    if len(models) == 0:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">No Models Available</div>
                <div class="card-subtitle">
                    No models found on your Ollama server. 
                    Go to the Model Management section to pull new models.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Models", len(models))
        
        # Calculate total size of all models in GB
        total_size_bytes = sum(model.get("size", 0) for model in models)
        total_size_gb = total_size_bytes / (1024 * 1024 * 1024)
        
        with col2:
            st.metric("Total Size", f"{total_size_gb:.2f} GB")
        
        # Find newest model by date
        newest_model = None
        newest_date = None
        
        for model in models:
            model_date = model.get("modified_at", "")
            if model_date and (newest_date is None or model_date > newest_date):
                newest_date = model_date
                newest_model = model.get("name", "Unknown")
        
        with col3:
            if newest_model:
                st.metric("Latest Model", newest_model)
        
        # Models grid display
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Available Models</div>", unsafe_allow_html=True)
        
        # Use columns to create a grid
        cols = st.columns(3)
        
        for i, model in enumerate(models):
            model_name = model.get("name", "Unknown")
            model_modified = model.get("modified_at", "Unknown")
            
            # Format modification date
            if model_modified != "Unknown":
                try:
                    modified_date = datetime.datetime.fromisoformat(model_modified.replace('Z', '+00:00'))
                    model_modified = modified_date.strftime("%Y-%m-%d %H:%M")
                except (ValueError, AttributeError):
                    pass
            
            # Calculate size in appropriate units
            size_bytes = model.get("size", 0)
            if size_bytes > 1024 * 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
            elif size_bytes > 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size_bytes / 1024:.2f} KB"
            
            # Check if model is an embedding model (contains 'bert' in family)
            is_embedding_model = False
            if "details" in model and "family" in model["details"]:
                family = model["details"]["family"].lower()
                is_embedding_model = "bert" in family
            
            with cols[i % 3]:
                # Truncate model name if too long (for display purposes only)
                display_name = model_name
                if len(model_name) > 25:
                    display_name = model_name[:22] + "..."
                
                # Construct model card with fixed dimensions
                card_content = f"""
                <div class="card">
                    <div class="card-title" title="{model_name}">{display_name}</div>
                    <div class="card-subtitle">
                        <strong>Size:</strong> {size_str}<br/>
                        <strong>Modified:</strong> {model_modified}<br/>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: auto; margin-bottom: 10px;">
                        <span class="status-indicator success"></span>
                        <span class="status-text">Available</span>
                    </div>
                </div>
                """
                
                st.markdown(card_content, unsafe_allow_html=True)
                
                # Add button container with Load and Delete buttons side by side
                col1, col2 = st.columns(2)
                
                # Add load button only for non-embedding models
                with col1:
                    if not is_embedding_model:
                        if st.button(f"Load (60m)", key=f"load_{model_name}", use_container_width=True):
                            with st.spinner(f"Loading {model_name} into VRAM..."):
                                result = api.load_model_into_vram(model_name, keep_alive="60m")
                                if "error" not in result:
                                    st.success(f"{model_name} loaded successfully for 60 minutes")
                                    time.sleep(1)  # Brief pause
                                    st.rerun()  # Refresh the page
                                else:
                                    st.error(f"Error: {result.get('error')}")
                    else:
                        # Placeholder button for embedding models (disabled)
                        st.button(f"Embedding Only", key=f"embedding_{model_name}", use_container_width=True, disabled=True)
                
                # Add delete button for all models
                with col2:
                    # Use a unique key for the delete button
                    delete_key = f"delete_{model_name}"
                    if st.button(f"Delete", key=delete_key, use_container_width=True, type="primary"):
                        # Use a session state variable to track which model is being deleted
                        if "delete_confirmation" not in st.session_state:
                            st.session_state.delete_confirmation = {}
                        
                        # Toggle the confirmation state for this model
                        st.session_state.delete_confirmation[model_name] = True
                        st.rerun()
                
                # Show confirmation outside the column nesting if needed
                if st.session_state.get("delete_confirmation", {}).get(model_name, False):
                    st.warning(f"Are you sure you want to delete {model_name}?")
                    
                    # Create buttons for confirmation (not nested in columns)
                    col_confirm, col_cancel = st.columns(2)
                    
                    with col_confirm:
                        if st.button("Yes, Delete", key=f"confirm_delete_{model_name}", use_container_width=True):
                            with st.spinner(f"Deleting {model_name}..."):
                                result = api.delete_model(model_name)
                                if "error" not in result:
                                    st.success(f"{model_name} deleted successfully")
                                    # Remove the confirmation state
                                    del st.session_state.delete_confirmation[model_name]
                                    time.sleep(1)  # Brief pause
                                    # Force refresh of models data
                                    st.session_state.models_data = api.list_models()
                                    st.rerun()  # Refresh the page
                                else:
                                    st.error(f"Error: {result.get('error')}")
                    
                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_delete_{model_name}", use_container_width=True):
                            # Remove the confirmation state
                            del st.session_state.delete_confirmation[model_name]
                            st.rerun()  # Refresh the page
        
        # Recent activity
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Server Information</div>", unsafe_allow_html=True)
        
        # Get server version info
        server_info = api.get_version()
        
        if "error" not in server_info:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-subtitle">
                        <strong>Version:</strong> {server_info.get('version', 'Unknown')}<br/>
                        <strong>Build:</strong> {server_info.get('build', 'Unknown')}<br/>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.error("Could not fetch server information.")
