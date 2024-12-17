# frontend/app.py
import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).parents[1]
sys.path.insert(0, str(root_dir))

# Page configuration must come before any other Streamlit commands
st.set_page_config(
    page_title="HealthTrack",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

from frontend.styles.styles import get_healthtrack_styles
from backend.database import init_db
from frontend.views.auth import render_login
from frontend.views.dashboard import render_dashboard
from frontend.views.records import render_records_view
from frontend.views.vitals import render_vitals_view
from frontend.views.medications import render_medications_view
from frontend.views.settings import render_settings_view

# Initialize database
init_db()

# Apply styles
st.markdown(get_healthtrack_styles(), unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'view' not in st.session_state:
    st.session_state.view = 'dashboard'

def render_navigation():
    st.sidebar.markdown("""
        <div class="nav-header">
            <h2>HealthTrack</h2>
        </div>
    """, unsafe_allow_html=True)

    nav_items = {
        "dashboard": {"icon": "📊", "label": "Dashboard"},
        "records": {"icon": "📁", "label": "Health Records"},
        "vitals": {"icon": "❤️", "label": "Vital Signs"},
        "medications": {"icon": "💊", "label": "Medications"},
        "settings": {"icon": "⚙️", "label": "Settings"}
    }

    for key, item in nav_items.items():
        is_active = st.session_state.view == key
        if st.sidebar.button(
            f"{item['icon']} {item['label']}", 
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.view = key
            st.rerun()

    # Add version info at bottom of sidebar
    st.sidebar.markdown("""
        <div class="sidebar-footer">
            <p>Version 1.0.0</p>
        </div>
    """, unsafe_allow_html=True)

def render_user_menu():
    cols = st.columns([6,2])
    with cols[1]:
        st.markdown(f"""
            <div class="user-menu">
                <span class="user-name">👤 {st.session_state.user['name']}</span>
                <span class="user-menu-icon">▾</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

def main():
    if not st.session_state.authenticated:
        render_login()
    else:
        render_user_menu()
        render_navigation()
        
        with st.container():
            if st.session_state.view == "dashboard":
                render_dashboard()
            elif st.session_state.view == "records":
                render_records_view()
            elif st.session_state.view == "vitals":
                render_vitals_view()
            elif st.session_state.view == "medications":
                render_medications_view()
            elif st.session_state.view == "settings":
                render_settings_view()

if __name__ == "__main__":
    main()