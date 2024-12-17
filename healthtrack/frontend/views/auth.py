# frontend/views/auth.py
import streamlit as st
from backend.auth import Auth

def render_login():
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h1>Welcome to HealthTrack</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit:
                if email and password:
                    user, message = Auth.login_user(email, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">{message}</div>', 
                                  unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div class="error-message">Please fill in all fields</div>',
                        unsafe_allow_html=True
                    )
    
    with tab2:
        with st.form("register_form", clear_on_submit=True):
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit:
                if all([name, email, password, confirm_password]):
                    if password == confirm_password:
                        success, message = Auth.register_user(email, password, name)
                        if success:
                            st.markdown(
                                f'<div class="success-message">{message}</div>',
                                unsafe_allow_html=True
                            )
                            st.rerun()
                        else:
                            st.markdown(
                                f'<div class="error-message">{message}</div>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            '<div class="error-message">Passwords do not match</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        '<div class="error-message">Please fill in all fields</div>',
                        unsafe_allow_html=True
                    )