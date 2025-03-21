import streamlit as st
import time
import pandas as pd
from datetime import datetime
import json
from utils.button_handler import handle_button_click

def render_model_management(api):
    """Render the model management interface with different tabs"""
    
    st.markdown("<div class='header-container'><h1 class='header-text'>Model Management</h1></div>", unsafe_allow_html=True)
    
    # Create tabs for different model management functions
    tabs = ["Models", "Pull New Model"]
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Models"
    
    # Draw the tab buttons manually
    cols = st.columns(len(tabs))
    for i, tab in enumerate(tabs):
        tab_class = "sidebar-item active" if st.session_state.active_tab == tab else "sidebar-item"
        cols[i].markdown(f"""
            <div class="{tab_class}" onclick="
                document.querySelector('.active').classList.remove('active');
                this.classList.add('active');
                const event = new CustomEvent('tabChange', {{ detail: {{ tab: '{tab}' }} }});
                window.dispatchEvent(event);
            ">
                {tab}
            </div>
        """, unsafe_allow_html=True)
        
        if cols[i].button(tab, key=f"tab_{tab}", help=f"Switch to {tab}", use_container_width=True):
            st.session_state.active_tab = tab
            st.rerun()
    
    # Display the active tab content
    if st.session_state.active_tab == "Models":
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fetch local models
        with st.spinner("Fetching models..."):
            success, local_models = api.list_local_models()
        
        if not success:
            st.error(f"Failed to fetch models: {local_models.get('error', 'Unknown error')}")
            return
        
        models = local_models.get("models", [])
        
        # Use our new model cards function
        render_model_cards(api, models)
    
    elif st.session_state.active_tab == "Pull New Model":
        st.markdown("<br>", unsafe_allow_html=True)
        # Pull New Model tab
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Pull a New Model</div>
                <div class="card-subtitle">
                    Download a model from the Ollama library to your local machine.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Popular models suggestions
        popular_models = [
            "llama3.1", "llama3.2", "mistral", "codellama:code", 
            "qwen2:4b", "llama2", "phi3:14b", "gemma:7b", "orca-mini"
        ]
        
        # Model input with suggestions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            model_name = st.text_input(
                "Model Name",
                placeholder="e.g., llama3.1:latest",
                help="Enter the model name and tag to pull (e.g., llama3.1:latest)"
            )
        
        with col2:
            suggested_model = st.selectbox(
                "Popular Models",
                options=["Select..."] + popular_models,
                index=0
            )
            
            if suggested_model != "Select...":
                model_name = suggested_model
        
        # Pull model button
        if st.button("Pull Model", key="pull_model_button"):
            if not model_name:
                st.error("Please enter a model name")
            else:
                # Create placeholders for progress tracking
                progress_container = st.container()
                detail_expander = progress_container.expander("View Download Details", expanded=False)
                progress_msg = progress_container.empty()
                progress_bar = progress_container.progress(0.0)
                details_placeholder = detail_expander.empty()
                
                # Initialize details
                current_file = ""
                download_speed = "0 KB/s"
                completed_size = 0
                total_size = 0
                
                # Show initial status
                progress_msg.info(f"Starting download of {model_name}...")
                details_placeholder.markdown("Initializing download...")
                
                try:
                    # Get streaming response
                    response_stream = api.pull_model(model_name, stream=True)
                    
                    # Initialize vars for tracking progress
                    download_start_time = time.time()
                    last_update_time = download_start_time
                    last_completed_size = 0
                    
                    # Process the stream
                    for chunk in response_stream.iter_lines():
                        if chunk:
                            try:
                                # Parse the JSON data
                                chunk_data = json.loads(chunk.decode('utf-8'))
                                
                                # Extract progress information
                                status = chunk_data.get("status", "")
                                
                                if "digest" in chunk_data:
                                    current_file = chunk_data.get("digest", "")[:12]  # First 12 chars of digest
                                
                                # Calculate completed and total (if available)
                                if "completed" in chunk_data and "total" in chunk_data:
                                    completed_size = chunk_data.get("completed", 0)
                                    total_size = chunk_data.get("total", 0)
                                    
                                    # Calculate progress percentage
                                    if total_size > 0:
                                        progress_percentage = min(completed_size / total_size, 1.0)
                                        progress_bar.progress(progress_percentage)
                                    
                                    # Calculate download speed (every second)
                                    current_time = time.time()
                                    if current_time - last_update_time >= 1.0:
                                        time_diff = current_time - last_update_time
                                        size_diff = completed_size - last_completed_size
                                        
                                        # Calculate speed in bytes/second
                                        speed = size_diff / time_diff
                                        
                                        # Format speed for display
                                        if speed >= 1024 * 1024:
                                            download_speed = f"{speed / (1024 * 1024):.2f} MB/s"
                                        else:
                                            download_speed = f"{speed / 1024:.2f} KB/s"
                                        
                                        # Update tracking variables
                                        last_update_time = current_time
                                        last_completed_size = completed_size
                                
                                # Update the display
                                if completed_size > 0 and total_size > 0:
                                    completed_mb = completed_size / (1024 * 1024)
                                    total_mb = total_size / (1024 * 1024)
                                    
                                    progress_msg.info(
                                        f"Downloading {model_name}: {completed_mb:.2f}/{total_mb:.2f} MB ({(completed_size/total_size*100):.1f}%)"
                                    )
                                    
                                    details_placeholder.markdown(
                                        f"""
                                        **Current Status:** {status}  
                                        **Current File:** {current_file}  
                                        **Download Speed:** {download_speed}  
                                        **Progress:** {completed_mb:.2f} MB of {total_mb:.2f} MB  
                                        **Elapsed Time:** {time.time() - download_start_time:.1f} seconds
                                        """
                                    )
                                elif status:
                                    # Just show the status if no size info
                                    progress_msg.info(f"Status: {status}")
                                    details_placeholder.markdown(
                                        f"""
                                        **Current Status:** {status}  
                                        **Current File:** {current_file}  
                                        **Elapsed Time:** {time.time() - download_start_time:.1f} seconds
                                        """
                                    )
                            except json.JSONDecodeError:
                                # Skip invalid JSON
                                pass
                    
                    # Show completion message
                    progress_bar.progress(1.0)
                    progress_msg.success(f"Model {model_name} pulled successfully!")
                    details_placeholder.markdown(
                        f"""
                        **Status:** Download Complete  
                        **Total Size:** {total_size / (1024 * 1024):.2f} MB  
                        **Total Time:** {time.time() - download_start_time:.1f} seconds  
                        **Average Speed:** {total_size / (1024 * 1024) / (time.time() - download_start_time):.2f} MB/s
                        """
                    )
                    
                    # Force refresh of models data
                    st.session_state.models_data = api.list_models()
                    
                except Exception as e:
                    progress_msg.error(f"Error pulling model: {str(e)}")
        
        # Progress indicator (note: for streaming progress, we would need WebSockets)
        st.markdown("<br/>", unsafe_allow_html=True)
        st.info("Note: Progress reporting for model downloads is limited in this interface. Check server logs for detailed progress.")

def render_model_cards(api, models_data):
    """Render model cards with status and pull button"""
    total_models = len(models_data)
    if total_models == 0:
        st.info("No models found. Pull a new model to get started.")
        return
    
    st.markdown(f"<div class='card-title'>Available Models ({total_models})</div>", unsafe_allow_html=True)
    
    # Create a grid layout for model cards - 3 per row
    cols_per_row = 3
    rows = (total_models + cols_per_row - 1) // cols_per_row  # Ceiling division
    
    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            model_idx = row * cols_per_row + col_idx
            if model_idx < total_models:
                model = models_data[model_idx]
                model_name = model.get("name", "Unknown")
                
                # Display name (truncate if too long)
                display_name = model_name
                if len(display_name) > 25:
                    display_name = display_name[:22] + "..."
                
                # Format the size
                size_bytes = model.get("size", 0)
                if size_bytes > 1_000_000_000:  # GB
                    size_str = f"{size_bytes / 1_000_000_000:.1f} GB"
                else:  # MB
                    size_str = f"{size_bytes / 1_000_000:.1f} MB"
                
                # Get model family if available
                family = model.get("family", "Unknown")
                
                # Get the last modified date - reformat to a more readable format
                if "modified_at" in model:
                    modified_timestamp = model.get("modified_at", 0) / 1_000_000_000  # Convert from nanoseconds
                    modified_date = datetime.fromtimestamp(modified_timestamp).strftime("%Y-%m-%d")
                    modified_str = f"Last modified: {modified_date}"
                else:
                    modified_str = "Last modified: Unknown"
                
                # Determine if the model is currently loaded
                success, running_models = api.list_running_models()
                is_running = False
                if success:
                    running_model_names = [rm.get("name", "") for rm in running_models.get("models", [])]
                    is_running = model_name in running_model_names
                
                # Create a card for the model with a consistent yellow background for dark mode
                with cols[col_idx]:
                    # Construct model card with yellow background for dark mode
                    card_content = f"""
                    <div class="model-card">
                        <div class="model-card-title">{display_name}</div>
                        <div class="model-card-subtitle">
                            <strong>Size:</strong> {size_str}<br/>
                            <strong>Family:</strong> {family}<br/>
                            {modified_str}
                        </div>
                        <div class="model-status">
                            <div><div class="model-status-indicator"></div></div>
                            <div class="model-status-text">Available</div>
                        </div>
                    </div>
                    """
                    st.markdown(card_content, unsafe_allow_html=True)
                    
                    # Create action buttons (load or delete) below the card
                    if st.session_state.get("active_tab") == "Models":
                        col1, col2 = st.columns(2)
                        with col1:
                            # If the model is running, show "Unload" instead of "Load"
                            if is_running:
                                if st.button("Unload", key=f"unload_{model_name}"):
                                    with st.spinner(f"Unloading model {model_name}..."):
                                        success, response = api.unload_model(model_name)
                                        if success:
                                            st.success(f"Successfully unloaded model {model_name}")
                                            st.rerun()
                                        else:
                                            st.error(f"Failed to unload model: {response.get('error', 'Unknown error')}")
                            else:
                                if st.button("Load (60m)", key=f"load_{model_name}"):
                                    with st.spinner(f"Loading model {model_name}..."):
                                        # Default to 60 minutes keep-alive time
                                        success, response = api.load_model(model_name, 60)
                                        if success:
                                            st.success(f"Successfully loaded model {model_name} (expires in 60 minutes)")
                                            st.rerun()
                                        else:
                                            st.error(f"Failed to load model: {response.get('error', 'Unknown error')}")
                        
                        # Add a delete button for all models
                        with col2:
                            if st.button("Delete", key=f"delete_{model_name}"):
                                with st.spinner(f"Deleting model {model_name}..."):
                                    success, response = api.delete_model(model_name)
                                    if success:
                                        st.success(f"Successfully deleted model {model_name}")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to delete model: {response.get('error', 'Unknown error')}")

# Model Details tab
def render_model_details(api):
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Model Details</div>
            <div class="card-subtitle">
                View detailed information about a specific model.
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Model selection for details
    detail_model = st.selectbox(
        "Select Model",
        options=["Select..."] + [model.get("name", "") for model in st.session_state.models_data],
        key="detail_model_select"
    )
    
    if st.button("View Details", key="view_details_button"):
        # Set button clicked state for future reference
        st.session_state.button_clicked["view_details_button"] = True
        
    # Check if button was clicked previously to avoid double-click issues
    if st.session_state.get("button_clicked", {}).get("view_details_button", False):
        st.session_state.button_clicked["view_details_button"] = False
        if detail_model == "Select...":
            st.error("Please select a model")
        else:
            with st.spinner(f"Fetching details for {detail_model}..."):
                details = api.get_model_details(detail_model)
                
                if "error" not in details:
                    # Display model details in a card
                    st.markdown(
                        f"""
                        <div class="card">
                            <div class="card-title">{detail_model}</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Format model parameters nicely
                    st.json(details)
                else:
                    st.error(f"Error fetching model details: {details.get('error')}")

# Manage Existing Models tab
def render_model_operations(api):
    # Display models table
    if not st.session_state.models_data:
        st.warning("No models available. Pull some models first.")
    else:
        # Create dataframe for better display
        models_data = []
        for model in st.session_state.models_data:
            model_name = model.get("name", "Unknown")
            size_bytes = model.get("size", 0)
            
            # Calculate size in appropriate units
            if size_bytes > 1024 * 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
            elif size_bytes > 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size_bytes / 1024:.2f} KB"
            
            modified = model.get("modified_at", "Unknown")
            # Format modification date
            if modified != "Unknown":
                try:
                    modified_date = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                    modified = modified_date.strftime("%Y-%m-%d %H:%M")
                except (ValueError, AttributeError):
                    pass
            
            models_data.append({
                "Model": model_name,
                "Size": size_str,
                "Modified": modified
            })
        
        # Create DataFrame
        df = pd.DataFrame(models_data)
        
        # Display with styling
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Model": st.column_config.TextColumn("Model"),
                "Size": st.column_config.TextColumn("Size"),
                "Modified": st.column_config.TextColumn("Last Modified")
            }
        )
        
        # Model operations
        st.markdown("<div class='card-title'>Model Operations</div>", unsafe_allow_html=True)
        
        # Simplified interface with single model selection
        selected_model = st.selectbox(
            "Select Model",
            options=["Select..."] + [model.get("name", "") for model in st.session_state.models_data],
            key="operations_model_select"
        )
        
        # Operation selection
        operation = st.selectbox(
            "Select Operation",
            options=["Select...", "Load Model into VRAM", "Unload Model from VRAM", "Delete Model"],
            key="model_operation"
        )
        
        # Conditional UI based on operation
        if operation == "Load Model into VRAM":
            keep_alive_options = {
                "5 minutes": "5m",
                "10 minutes": "10m",
                "30 minutes": "30m",
                "1 hour": "1h",
                "4 hours": "4h",
                "Indefinite": "1d",
                "Custom (minutes)": "custom"
            }
            
            keep_alive = st.selectbox(
                "Keep Alive Duration",
                options=list(keep_alive_options.keys()),
                index=0,
                key="keep_alive_select"
            )
            
            # Add custom minutes input field if "Custom" is selected
            custom_minutes = None
            if keep_alive == "Custom (minutes)":
                custom_minutes = st.number_input(
                    "Enter custom duration in minutes",
                    min_value=1,
                    value=30,
                    help="Enter the number of minutes to keep the model loaded in VRAM",
                    key="custom_minutes_input"
                )
            
            operation_button = st.button("Load Model", key="load_model_button", type="primary")
            
            if operation_button:
                # Set button clicked state for future reference
                st.session_state.button_clicked["load_model_button"] = True
                
            # Check if button was clicked previously to avoid double-click issues
            if operation_button or handle_button_click("load_model_button"):
                if selected_model == "Select...":
                    st.error("Please select a model")
                else:
                    # Process keep_alive value
                    keep_alive_value = keep_alive_options[keep_alive]
                    if keep_alive == "Custom (minutes)":
                        keep_alive_value = f"{custom_minutes}m"
                        
                    with st.spinner(f"Loading model {selected_model} into VRAM..."):
                        result = api.load_model_into_vram(
                            selected_model, 
                            keep_alive=keep_alive_value
                        )
                        
                        if "error" not in result:
                            st.success(f"Model {selected_model} loaded successfully with keep-alive time of {keep_alive}!")
                        else:
                            st.error(f"Error loading model: {result.get('error')}")

        elif operation == "Unload Model from VRAM":
            st.info("This will immediately unload the model from VRAM by setting keep-alive to 0 seconds.")
            
            operation_button = st.button("Unload Model", key="unload_model_button", type="primary")
            
            if operation_button:
                # Set button clicked state for future reference
                st.session_state.button_clicked["unload_model_button"] = True
                
            # Check if button was clicked previously to avoid double-click issues
            if operation_button or handle_button_click("unload_model_button"):
                if selected_model == "Select...":
                    st.error("Please select a model")
                else:
                    with st.spinner(f"Unloading model {selected_model} from VRAM..."):
                        result = api.remove_model_from_vram(selected_model)
                        
                        if "error" not in result:
                            st.success(f"Model {selected_model} unloaded successfully from VRAM!")
                        else:
                            st.error(f"Error unloading model: {result.get('error')}")

        elif operation == "Delete Model":
            st.warning("⚠️ Warning: This action cannot be undone. The model will be permanently deleted from your system.")
            
            # Confirmation checkbox
            confirm_delete = st.checkbox("I confirm that I want to delete this model", key="confirm_delete")
            
            operation_button = st.button("Delete Model", key="delete_model_button", type="primary", disabled=not confirm_delete)
            
            if operation_button:
                # Set button clicked state for future reference
                st.session_state.button_clicked["delete_model_button"] = True
                
            # Check if button was clicked previously to avoid double-click issues
            if operation_button or handle_button_click("delete_model_button"):
                if selected_model == "Select...":
                    st.error("Please select a model")
                elif not confirm_delete:
                    st.error("Please confirm deletion")
                else:
                    with st.spinner(f"Deleting model {selected_model}..."):
                        result = api.delete_model(selected_model)
                        
                        if "error" not in result:
                            st.success(f"Model {selected_model} deleted successfully!")
                            # Force refresh of models data
                            st.session_state.models_data = api.list_models()
                            time.sleep(1)  # Brief pause to ensure UI updates
                            st.rerun()  # Refresh the page to update model list
                        else:
                            st.error(f"Error deleting model: {result.get('error')}")

        elif operation != "Select...":
            st.info("Please select an operation from the dropdown above.")
