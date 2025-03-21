import streamlit as st

def hide_streamlit_footer():
    """Injects custom CSS and JavaScript to permanently hide the Streamlit footer."""
    # CSS to hide the footer element
    hide_footer_style = """
    <style>
        footer {display: none !important;}
        footer:after {visibility: hidden !important;}
        
        /* Hide specific Streamlit elements */
        .viewerBadge_container__1QSob {display: none !important;}
        .styles_viewerBadge__1yB5_ {display: none !important;}
        .styles_viewerBadge__1yB5_ span {display: none !important;}
        .stDeployButton {display: none !important;}
        #MainMenu {display: none !important;}
        header {display: none !important;}
        
        /* Remove padding that would otherwise add whitespace */
        .block-container {padding-bottom: 0px !important;}
        .css-1544g2n.e1fqkh3o4 {padding-top: 2rem;}
    </style>
    """
    
    # JavaScript to remove footer elements after the page loads
    hide_footer_js = """
    <script>
        // Function to remove footer
        function removeFooter() {
            const footers = document.getElementsByTagName('footer');
            for(let i = 0; i < footers.length; i++) {
                footers[i].style.display = 'none';
            }
            
            // Remove elements containing specific text
            const all = document.getElementsByTagName('*');
            for (let i = 0; i < all.length; i++) {
                if (all[i].innerText && 
                   (all[i].innerText.includes('Built with Streamlit') || 
                    all[i].innerText.includes('Apple-inspired UI'))) {
                    all[i].style.display = 'none';
                }
            }
        }
        
        // Run on page load
        removeFooter();
        
        // Run again after small delay to catch dynamically loaded elements
        setTimeout(removeFooter, 500);
        
        // Add a mutation observer to handle dynamic content
        const observer = new MutationObserver(function(mutations) {
            removeFooter();
        });
        
        // Start observing the document body for DOM changes
        observer.observe(document.body, { 
            childList: true,
            subtree: true
        });
    </script>
    """
    
    # Inject CSS and JavaScript
    st.markdown(hide_footer_style, unsafe_allow_html=True)
    st.markdown(hide_footer_js, unsafe_allow_html=True)
