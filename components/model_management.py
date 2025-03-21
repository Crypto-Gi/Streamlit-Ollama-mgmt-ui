import streamlit as st
import time
import pandas as pd
from datetime import datetime
import json

def render_model_management(api):
    """Render the model management interface with pull, delete, and detail options"""
    
    st.markdown("<div class='card-title'>Model Management</div>", unsafe_allow_html=True)
    
    # Check if API is connected first
    if not st.session_state.get("api_connected", False):
        st.warning("Not connected to Ollama server. Please configure and test your connection in the sidebar.")
        
        # Display example connection instructions
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Connection Required</div>
                <div class="card-subtitle">
                    You need to connect to an Ollama server to manage models.
                    Please configure and test your connection in the sidebar.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
    
    # Create tabs for different management functions
    tab1, tab2, tab3 = st.tabs(["Pull New Model", "Manage Existing Models", "Model Details"])
    
    # Pull New Model tab
    with tab1:
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
    
    # Manage Existing Models tab
    with tab2:
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
    
    # Model Details tab
    with tab3:
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
