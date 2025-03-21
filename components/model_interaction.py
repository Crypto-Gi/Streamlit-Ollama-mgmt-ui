import streamlit as st
import time
import json

def render_model_interaction(api):
    """Render the model interaction interface for chat with models"""
    
    st.markdown("<div class='card-title'>Model Interaction</div>", unsafe_allow_html=True)
    
    # Check if API is connected first
    if not st.session_state.get("api_connected", False):
        st.warning("Not connected to Ollama server. Please configure and test your connection in the sidebar.")
        
        # Display example connection instructions
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Connection Required</div>
                <div class="card-subtitle">
                    You need to connect to an Ollama server to interact with models.
                    Please configure and test your connection in the sidebar.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        return
    
    # Initialize chat history in session state if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Model selection
    model_options = ["Select..."] + [model.get("name", "") for model in st.session_state.models_data]
    selected_model = st.selectbox("Select Model", options=model_options)
    
    # Chat interface container
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Chat Interface</div>
            <div class="card-subtitle">
                Interact with your selected model through a chat interface.
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                        <div style="background-color: #0A84FF33; padding: 0.8rem; border-radius: 15px 15px 0 15px; max-width: 80%;">
                            {content}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                        <div style="background-color: #323232; padding: 0.8rem; border-radius: 15px 15px 15px 0; max-width: 80%;">
                            {content}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
    
    # Input area
    st.markdown("<br/>", unsafe_allow_html=True)
    
    with st.container():
        # Text input for prompt
        user_prompt = st.text_area(
            "Your message",
            placeholder="Type your message here...",
            key="user_prompt",
            height=100
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=2.0,
                    value=0.7,
                    step=0.1,
                    help="Lower values make responses more deterministic, higher values make them more creative"
                )
            
            with col2:
                context_length = st.select_slider(
                    "Context Length",
                    options=[2048, 4096, 8192, 16384, 32768],
                    value=4096,
                    help="Maximum number of tokens to use for context. Higher values allow the model to consider more conversation history."
                )
            
            stream_response = st.checkbox(
                "Stream Response",
                value=True,
                help="Stream the response token by token"
            )
        
        # Submit button
        col1, col2 = st.columns([6, 1])
        
        with col2:
            submit = st.button("Send", type="primary")
        
        with col1:
            clear_chat = st.button("Clear Chat")
            
        # Handle clear chat
        if clear_chat:
            st.session_state.chat_history = []
            st.rerun()
        
        # Handle message submission
        if submit:
            if selected_model == "Select...":
                st.error("Please select a model first")
            elif not user_prompt:
                st.error("Please enter a message")
            else:
                # Add user message to chat history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_prompt
                })
                
                # Create a placeholder for the assistant's response
                with st.spinner(f"Generating response from {selected_model}..."):
                    if stream_response:
                        # For streaming response
                        response_placeholder = st.empty()
                        full_response = ""
                        
                        try:
                            # Pass the existing chat history to provide context
                            response_stream = api.generate_response(
                                selected_model,
                                user_prompt,
                                temperature=temperature,
                                context_length=context_length,
                                chat_history=st.session_state.chat_history[:-1],  # Exclude the most recent message
                                stream=True
                            )
                            
                            # We're using a streaming response, so we need to iterate through the chunks
                            for chunk in response_stream.iter_lines():
                                if chunk:
                                    chunk_data = json.loads(chunk.decode('utf-8'))
                                    response_text = chunk_data.get("response", "")
                                    full_response += response_text
                                    
                                    # Update the placeholder with the accumulated response
                                    response_placeholder.markdown(
                                        f"""
                                        <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                                            <div style="background-color: #323232; padding: 0.8rem; border-radius: 15px 15px 15px 0; max-width: 80%;">
                                                {full_response}
                                            </div>
                                        </div>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                                    
                                    # Check if the response is done
                                    if chunk_data.get("done", False):
                                        break
                            
                            # Add the assistant's response to chat history
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": full_response
                            })
                            
                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")
                    else:
                        # For non-streaming response
                        try:
                            response = api.generate_response(
                                selected_model,
                                user_prompt,
                                temperature=temperature,
                                context_length=context_length,
                                chat_history=st.session_state.chat_history[:-1],  # Exclude the most recent message
                                stream=False
                            )
                            
                            if "error" not in response:
                                response_text = response.get("response", "")
                                
                                # Add the assistant's response to chat history
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": response_text
                                })
                            else:
                                st.error(f"Error: {response.get('error')}")
                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")
                
                # Rerun the app to update the chat history
                st.rerun()
    
    # Model parameters
    st.markdown("<br/>", unsafe_allow_html=True)
    if selected_model != "Select...":
        with st.expander("Model Information"):
            st.markdown(
                f"""
                <div class="card-subtitle">
                    <strong>Selected Model:</strong> {selected_model}<br/>
                    <strong>Temperature:</strong> {temperature}<br/>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.info("For more detailed model information, visit the Model Details tab in the Model Management section.")
