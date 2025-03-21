"""Custom styling for the Streamlit Ollama UI."""

import streamlit as st

def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app."""
    # Check if dark mode is enabled
    is_dark_mode = st.session_state.get("dark_mode", False)
    
    # Define color palettes for dark and light modes
    if is_dark_mode:
        # Dark mode colors based exactly on the user's second image - consistent navy throughout
        colors = {
            "background": "#0B0F2B",            # Deep navy background for entire UI
            "card_bg": "#131A4E",               # Slightly lighter navy for cards
            "sidebar_bg": "#07091E",            # Darker navy for sidebar
            "accent_blue": "#3366FF",           # Vibrant blue accent
            "text_primary": "#FFFFFF",          # Pure white for primary text
            "text_secondary": "#A4B1E1",        # Light blue-gray for secondary text
            "success_green": "#00C853",         # Bright green for success states
            "warning_orange": "#FFB300",        # Amber/orange for warnings
            "error_red": "#FF3D71",             # Bright red for errors
            "highlight_yellow": "#FFB74D",      # Yellow for model cards
            "border": "#273069",                # Subtle border for dark mode
            "button_bg": "#1A237E",             # Dark blue button
            "button_hover": "#283593",          # Slightly lighter blue on hover
            "card_shadow": "rgba(0, 0, 0, 0.2)" # Subtle shadow
        }
    else:
        # Light mode colors remain unchanged
        colors = {
            "background": "#F8FAFC",            # Very light blue-gray
            "card_bg": "#FFFFFF",               # White for cards
            "sidebar_bg": "#F1F5F9",            # Light gray for sidebar
            "accent_blue": "#1A73E8",           # Google blue
            "text_primary": "#202124",          # Dark gray for primary text
            "text_secondary": "#5F6368",        # Medium gray for secondary text
            "success_green": "#34A853",         # Google green
            "warning_orange": "#FBBC04",        # Google yellow
            "error_red": "#EA4335",             # Google red
            "border": "#DADCE0",                # Light gray border
            "button_bg": "#F1F3F4",             # Very light gray button
            "button_hover": "#E8EAED",          # Slightly darker on hover
            "card_shadow": "rgba(60, 64, 67, 0.1)", # Light shadow
            "highlight_teal": "#00A9A7",         # Teal highlight color
            "highlight_purple": "#A142F4"        # Purple highlight color
        }
    
    # Apply the custom CSS
    st.markdown(f"""
    <style>
        /* Base Theme Overrides */
        .stApp {{
            background-color: {colors["background"]};
            color: {colors["text_primary"]};
        }}
        
        /* Make everything dark in dark mode - main content area too */
        .main .block-container {{
            background-color: {colors["background"] if is_dark_mode else "transparent"};
            padding: 2rem !important;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* Improve sidebar styling */
        .sidebar .sidebar-content {{
            background-color: {colors["sidebar_bg"]};
            border-right: {f"1px solid {colors['border']}" if is_dark_mode else "none"};
        }}
        
        /* Header Styling with Gradient */
        .header-container {{
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            background-color: {colors["card_bg"]};
            border-radius: 12px;
            text-align: center;
            box-shadow: {("0 8px 16px rgba(0, 0, 0, 0.3)" if is_dark_mode else "none")};
            border: {("1px solid rgba(255, 255, 255, 0.1)" if is_dark_mode else "none")};
        }}
        
        .header-text {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: {colors["text_primary"]} !important;
            margin: 0 !important;
            letter-spacing: 0.5px;
        }}
        
        /* Card Styling */
        .card {{
            background-color: {colors["card_bg"]};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: {("1px solid rgba(255, 255, 255, 0.05)" if is_dark_mode else f"1px solid {colors['border']}")};
            box-shadow: {("0 8px 24px rgba(0, 0, 0, 0.4)" if is_dark_mode else f"0 4px 16px {colors['card_shadow']}")};
            transition: all 0.3s ease;
            height: 200px;  /* Fixed height for all cards */
            display: flex;
            flex-direction: column;
        }}
        
        .card:hover {{
            box-shadow: {("0 12px 28px rgba(0, 0, 0, 0.5)" if is_dark_mode else f"0 6px 24px {colors['card_shadow']}")};
            transform: translateY(-2px);
        }}
        
        /* In dark mode, make specific metric cards with vibrant colors */
        .metric-card-yellow {{
            background: {("linear-gradient(45deg, #FFAF1B, #FFD875)" if is_dark_mode else colors["card_bg"])};
            color: {("#000000" if is_dark_mode else colors["text_primary"])};
        }}
        
        .metric-card-blue {{
            background: {("linear-gradient(45deg, #4174FF, #81A5FF)" if is_dark_mode else colors["card_bg"])};
            color: {("#FFFFFF" if is_dark_mode else colors["text_primary"])};
        }}
        
        .metric-card-pink {{
            background: {("linear-gradient(45deg, #FF3A8C, #FF7AA9)" if is_dark_mode else colors["card_bg"])};
            color: {("#FFFFFF" if is_dark_mode else colors["text_primary"])};
        }}
        
        .card-title {{
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
            color: {colors["text_primary"]} !important;
        }}
        
        .card-subtitle {{
            font-size: 0.9rem !important;
            color: {colors["text_secondary"]} !important;
            margin-bottom: 1rem !important;
        }}
        
        .card-value {{
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
            color: {colors["text_primary"]} !important;
        }}
        
        .card-label {{
            font-size: 0.9rem !important;
            color: {colors["text_secondary"]} !important;
        }}
        
        /* UI Elements */
        .stButton button {{
            background-color: {colors["button_bg"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["border"]};
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stButton button:hover {{
            background-color: {colors["button_hover"]};
            border-color: {colors["accent_blue"]};
        }}
        
        .stSelectbox {{
            background-color: {colors["card_bg"]};
            border-radius: 4px;
            border: 1px solid {colors["border"]};
        }}
        
        .load-button {{
            background-color: {colors["button_bg"] if not is_dark_mode else "#1A237E"};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            width: 100%;
            transition: all 0.2s ease;
        }}
        
        .load-button:hover {{
            background-color: {colors["button_hover"] if not is_dark_mode else "#283593"};
        }}
        
        .delete-button {{
            background-color: {colors["error_red"] if not is_dark_mode else "#1A237E"};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            width: 100%;
            transition: all 0.2s ease;
        }}
        
        .delete-button:hover {{
            background-color: {f"{colors['error_red']}DD" if not is_dark_mode else "#283593"};
        }}
        
        /* Model cards for dark mode - yellow cards like in the first image */
        .model-card {{
            background-color: {colors["highlight_yellow"] if is_dark_mode else colors["card_bg"]};
            color: {("#000000" if is_dark_mode else colors["text_primary"])};
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: {("none" if is_dark_mode else f"1px solid {colors['border']}")};
            box-shadow: {("0 4px 12px rgba(0, 0, 0, 0.3)" if is_dark_mode else f"0 2px 8px {colors['card_shadow']}")};
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            min-height: 160px;
            display: flex;
            flex-direction: column;
        }}
        
        .model-card:hover {{
            box-shadow: {("0 8px 20px rgba(0, 0, 0, 0.4)" if is_dark_mode else f"0 4px 16px {colors['card_shadow']}")};
            transform: translateY(-2px);
        }}
        
        .model-card-title {{
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.75rem !important;
            color: #000000 !important;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .model-card-subtitle {{
            font-size: 0.85rem !important;
            color: #000000 !important;
            opacity: 0.8;
            margin-bottom: 0.75rem !important;
            flex-grow: 1;
        }}
        
        .model-status {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
        }}
        
        .model-status-indicator {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: #00C853;
            display: inline-block;
            margin-right: 6px;
        }}
        
        .model-status-text {{
            font-size: 0.85rem;
            font-weight: 500;
            color: #000000;
        }}
        
        /* Status Indicator */
        .status-indicator {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }}
        
        .status-connected {{
            background-color: {colors["success_green"]};
        }}
        
        .status-disconnected {{
            background-color: {colors["error_red"]};
        }}
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {colors["sidebar_bg"]};
            border-right: {("none" if is_dark_mode else f"1px solid {colors['border']}")};
        }}
        
        .sidebar-item {{
            background-color: {colors["card_bg"] if is_dark_mode else colors["button_bg"]};
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            color: {colors["text_primary"]};
            border: {("1px solid rgba(255, 255, 255, 0.1)" if is_dark_mode else f"1px solid {colors['border']}")};
        }}
        
        .sidebar-item:hover {{
            background-color: {colors["accent_blue"] if is_dark_mode else colors["button_hover"]};
            color: white;
        }}
        
        .sidebar-item.active {{
            background-color: {colors["accent_blue"]};
            color: white;
        }}
        
        /* Fix Streamlit default elements */
        .stAlert {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-radius: 10px;
            border: {("1px solid rgba(255, 255, 255, 0.05)" if is_dark_mode else f"1px solid {colors['border']}")};
        }}
        
        .stTextInput input, .stNumberInput input, .stTextArea textarea {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border: {("1px solid rgba(255, 255, 255, 0.1)" if is_dark_mode else f"1px solid {colors['border']}")};
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
        }}
        
        .stDataFrame {{
            background-color: {colors["card_bg"]};
            border-radius: 10px;
            border: {("1px solid rgba(255, 255, 255, 0.05)" if is_dark_mode else f"1px solid {colors['border']}")};
        }}
        
        .stDataFrame table {{
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .stDataFrame th {{
            background-color: {colors["sidebar_bg"] if is_dark_mode else "#F1F5F9"};
            color: {colors["text_primary"]};
            border-bottom: {("1px solid rgba(255, 255, 255, 0.1)" if is_dark_mode else f"1px solid {colors['border']}")};
        }}
        
        /* Make stMetric darker and more consistent */
        div.stMetric {{
            background-color: {colors["card_bg"]};
            border-radius: 12px;
            padding: 1rem 1.25rem;
            box-shadow: {("0 4px 12px rgba(0, 0, 0, 0.3)" if is_dark_mode else "none")};
            border: {("1px solid rgba(255, 255, 255, 0.05)" if is_dark_mode else "none")};
        }}
        
        div.stMetric label, div.stMetric p {{
            color: {colors["text_primary"]}!important;
        }}
        
        /* Input Field Styling */
        .stTextInput > div > div > input {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-color: {colors["border"]};
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {colors["accent_blue"]};
            box-shadow: 0 0 0 1px {colors["accent_blue"]};
        }}
        
        /* Textarea Styling */
        .stTextArea > div > div > textarea {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-color: {colors["border"]};
        }}
        
        .stTextArea > div > div > textarea:focus {{
            border-color: {colors["accent_blue"]};
            box-shadow: 0 0 0 1px {colors["accent_blue"]};
        }}
        
        /* Slider Styling */
        .stSlider > div > div > div > div {{
            background-color: {colors["accent_blue"]};
        }}
        
        /* Select box Styling */
        .stSelectbox > div > div > div {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-color: {colors["border"]};
        }}
        
        .stSelectbox > div > div > div:focus {{
            border-color: {colors["accent_blue"]};
            box-shadow: 0 0 0 1px {colors["accent_blue"]};
        }}
        
        /* Multiselect Styling */
        .stMultiSelect > div > div > div {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-color: {colors["border"]};
        }}
        
        .stMultiSelect > div > div > div:focus {{
            border-color: {colors["accent_blue"]};
            box-shadow: 0 0 0 1px {colors["accent_blue"]};
        }}
        
        /* Date Input Styling */
        .stDateInput > div > div > div {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-color: {colors["border"]};
        }}
        
        .stDateInput > div > div > div:focus {{
            border-color: {colors["accent_blue"]};
            box-shadow: 0 0 0 1px {colors["accent_blue"]};
        }}
        
        /* Table Styling */
        .stDataFrame {{
            background-color: {colors["card_bg"]};
            color: {colors["text_primary"]};
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .stDataFrame table {{
            border-collapse: collapse;
            width: 100%;
        }}
        
        .stDataFrame thead th {{
            background-color: {colors["sidebar_bg"]};
            color: {colors["text_primary"]};
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid {colors["border"]};
        }}
        
        .stDataFrame tbody td {{
            padding: 1rem;
            border-bottom: 1px solid {colors["border"]};
        }}
        
        .stDataFrame tbody tr:hover {{
            background-color: {f"{colors['sidebar_bg']}77"};
        }}
        
        /* Chart customization for dark mode */
        .dark-chart {{
            filter: {("hue-rotate(25deg) saturate(150%)" if is_dark_mode else "none")};
        }}
        
        /* Vibrant progress bars for dark mode */
        .progress-bar-vibrant {{
            background: {("linear-gradient(90deg, " + colors['highlight_yellow'] + ", " + colors['accent_blue'] + ")" if is_dark_mode else colors["accent_blue"])};
            height: 8px;
            border-radius: 4px;
            margin: 8px 0;
        }}
        
        /* Custom expander styling */
        .streamlit-expanderHeader {{
            background-color: {colors["card_bg"]};
            border-radius: 8px;
            border: none;
            box-shadow: 0 2px 8px {colors["card_shadow"]};
            padding: 1rem !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            background-color: {f"{colors['card_bg']}DD"};
        }}
        
        .streamlit-expanderContent {{
            background-color: {colors["card_bg"]};
            border-radius: 0 0 8px 8px;
            border-top: none;
            padding: 1rem !important;
        }}
        
        /* Clean up Streamlit footer */
        .viewerBadge_link__1S137, footer, footer:after {{
            display: none !important;
        }}
        
        /* Version marker in footer */
        .version-info {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 12px;
            color: {colors["text_secondary"]};
            opacity: 0.7;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add version info
    version = "2.0.0"
    st.markdown(f"""
    <div class="version-info">v{version}</div>
    """, unsafe_allow_html=True)
