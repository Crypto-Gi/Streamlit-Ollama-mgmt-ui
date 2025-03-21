import streamlit as st

def apply_custom_styling():
    """Apply custom Apple-inspired dark mode styling"""
    
    # Define Apple-inspired color variables
    colors = {
        "background": "#161616",
        "card_bg": "#232323",
        "sidebar_bg": "#1c1c1e",
        "accent_blue": "#0a84ff",
        "accent_gradient_start": "#0A84FF",
        "accent_gradient_end": "#6F41E8",
        "text_primary": "#ffffff",
        "text_secondary": "#8a8a8e",
        "success_green": "#30d158",
        "warning_orange": "#ff9f0a",
        "error_red": "#ff453a",
        "border": "#38383A",
        "button_bg": "#323232",
        "button_hover": "#3A3A3C",
        "card_shadow": "rgba(0, 0, 0, 0.3)"
    }
    
    # Custom CSS with Apple-inspired styling
    st.markdown(f"""
    <style>
        /* Base Theme Overrides */
        .stApp {{
            background-color: {colors["background"]};
            color: {colors["text_primary"]};
        }}
        
        /* Header Styling with Gradient */
        .header-container {{
            padding: 1.5rem 0;
            margin-bottom: 1.5rem;
            border-radius: 12px;
            background: linear-gradient(135deg, {colors["accent_gradient_start"]}22, {colors["accent_gradient_end"]}22);
            border: 1px solid {colors["border"]};
        }}
        
        .header-text {{
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            padding: 0 1rem !important;
            background: linear-gradient(135deg, {colors["accent_gradient_start"]}, {colors["accent_gradient_end"]});
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            display: inline-block !important;
        }}
        
        .subheader-text {{
            font-size: 1.1rem !important;
            opacity: 0.8 !important;
            margin: 0.5rem 0 0 0 !important;
            padding: 0 1rem !important;
            color: {colors["text_secondary"]} !important;
        }}
        
        /* Card Styling */
        .card {{
            background-color: {colors["card_bg"]};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid {colors["border"]};
            box-shadow: 0 4px 16px {colors["card_shadow"]};
            transition: all 0.3s ease;
            height: 200px;  /* Fixed height for all cards */
            display: flex;
            flex-direction: column;
        }}
        
        .card:hover {{
            box-shadow: 0 6px 24px {colors["card_shadow"]};
            transform: translateY(-2px);
        }}
        
        .card-title {{
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            color: {colors["text_primary"]} !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}
        
        .card-subtitle {{
            font-size: 0.9rem !important;
            color: {colors["text_secondary"]} !important;
            margin-bottom: 1rem !important;
            flex-grow: 1;
        }}
        
        /* Card buttons */
        .card-buttons {{
            display: flex;
            justify-content: space-between;
            margin-top: auto;
        }}
        
        .load-button {{
            background-color: {colors["accent_blue"]};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s ease;
            flex: 1;
            margin-right: 5px;
        }}
        
        .load-button:hover {{
            background-color: {colors["accent_blue"]}CC;
        }}
        
        .delete-button {{
            background-color: {colors["error_red"]};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s ease;
            flex: 1;
            margin-left: 5px;
        }}
        
        .delete-button:hover {{
            background-color: {colors["error_red"]}CC;
        }}
        
        /* Status Indicator */
        .status-indicator {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 6px;
        }}
        
        .status-indicator.success {{
            background-color: {colors["success_green"]};
            box-shadow: 0 0 5px {colors["success_green"]}99;
        }}
        
        .status-indicator.warning {{
            background-color: {colors["warning_orange"]};
            box-shadow: 0 0 5px {colors["warning_orange"]}99;
        }}
        
        .status-indicator.error {{
            background-color: {colors["error_red"]};
            box-shadow: 0 0 5px {colors["error_red"]}99;
        }}
        
        .status-text {{
            display: inline-block;
            vertical-align: middle;
        }}
        
        /* Button Styling */
        .stButton>button {{
            background: {colors["button_bg"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["border"]};
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stButton>button:hover {{
            background: {colors["button_hover"]};
            border-color: {colors["accent_blue"]};
        }}
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {colors["sidebar_bg"]};
            border-right: 1px solid {colors["border"]};
        }}
        
        .sidebar-item {{
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .sidebar-item:hover {{
            background-color: {colors["accent_blue"]}22;
        }}
        
        .sidebar-item.active {{
            background-color: {colors["accent_blue"]}33;
            border-left: 3px solid {colors["accent_blue"]};
        }}
        
        /* Input Field Styling */
        .stTextInput>div>div>input {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["border"]};
            border-radius: 8px;
        }}
        
        .stTextInput>div>div>input:focus {{
            border-color: {colors["accent_blue"]};
            box-shadow: 0 0 0 1px {colors["accent_blue"]};
        }}
        
        /* Slider Styling */
        .stSlider>div>div>div>div {{
            background-color: {colors["accent_blue"]};
        }}
        
        /* Select Box Styling */
        .stSelectbox>div>div {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["border"]};
            border-radius: 8px;
        }}
        
        /* Progress Bar Styling */
        .stProgress>div>div>div>div {{
            background-color: {colors["accent_blue"]};
        }}
        
        /* Table Styling */
        .stTable {{
            border-radius: 12px;
            overflow: hidden;
        }}
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: {colors["text_primary"]} !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: 0.9rem !important;
            color: {colors["text_secondary"]} !important;
        }}
        
        /* Code Block Styling */
        .stCodeBlock {{
            border-radius: 8px;
            background-color: #1e1e1e;
        }}
        
        /* Tooltip */
        .tooltip {{
            position: relative;
            display: inline-block;
        }}
        
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 120px;
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            text-align: center;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
            border: 1px solid {colors["border"]};
        }}
        
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
        
        /* Divider */
        hr {{
            height: 1px;
            background-color: {colors["border"]};
            border: none;
            margin: 1.5rem 0;
        }}
        
        /* Custom overrides for Streamlit spacing */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }}
        
        /* Make metrics more compact */
        .stMetric {{
            margin-bottom: 0.5rem !important;
        }}
        
        /* Reduce spacing between elements */
        .element-container {{
            margin-bottom: 0.5rem !important;
        }}
        
        /* Streamlit footer (completely hide it) */
        footer {{visibility: hidden !important;}}
        header {{visibility: hidden !important;}}
        #MainMenu {{visibility: hidden !important;}}
        
        /* Custom footer positioning - move to bottom of page */
        .custom-footer {{
            position: fixed;
            bottom: 5px;
            right: 10px;
            opacity: 0.2;
            z-index: -1000;
            font-size: 0.6rem !important;
            color: #8a8a8e !important;
        }}
    </style>
    """, unsafe_allow_html=True)
