import streamlit as st

def handle_button_click(button_key):
    """
    Helper function to handle button clicks and prevent double-click issues.
    This provides a more reliable button interaction experience.
    
    Args:
        button_key (str): Unique key for the button
        
    Returns:
        bool: True if button action should be performed, False otherwise
    """
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = {}
        
    if button_key not in st.session_state.button_clicked:
        st.session_state.button_clicked[button_key] = False
        return False
    
    was_clicked = st.session_state.button_clicked[button_key]
    st.session_state.button_clicked[button_key] = False
    return was_clicked
