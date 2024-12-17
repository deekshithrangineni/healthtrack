# frontend/views/settings.py
import streamlit as st
from backend.models import HealthData
from backend.validators import Validators
from backend.auth import Auth

def render_settings_view():
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h1>Settings & Profile</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Profile Settings
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Profile Information</h2>
    """, unsafe_allow_html=True)
    
    with st.form("profile_form"):
        current_user = HealthData.get_user_profile(st.session_state.user['id'])
        
        name = st.text_input("Full Name", value=current_user['name'])
        email = st.text_input("Email", value=current_user['email'])
        
        col1, col2 = st.columns(2)
        with col1:
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", [
                "Male", "Female", "Non-binary", "Prefer not to say"
            ])
        
        with col2:
            height = st.number_input("Height (inches)")
            blood_type = st.selectbox("Blood Type", [
                "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
            ])
        
        if st.form_submit_button("Update Profile"):
            success = HealthData.update_user_profile(
                st.session_state.user['id'],
                name,
                email,
                dob,
                gender,
                height,
                blood_type
            )
            if success:
                st.markdown(
                    '<div class="success-message">Profile updated successfully!</div>',
                    unsafe_allow_html=True
                )
                st.session_state.user['name'] = name
                st.rerun()
            else:
                st.markdown(
                    '<div class="error-message">Failed to update profile</div>',
                    unsafe_allow_html=True
                )
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Security Settings
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Security Settings</h2>
    """, unsafe_allow_html=True)
    
    with st.form("security_form"):
        current_password = st.text_input(
            "Current Password",
            type="password"
        )
        new_password = st.text_input(
            "New Password",
            type="password"
        )
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )
        
        enable_mfa = st.checkbox(
            "Enable Two-Factor Authentication",
            value=current_user.get('mfa_enabled', False)
        )
        
        if st.form_submit_button("Update Security Settings"):
            updates_made = False
            
            # Handle password update
            if current_password and new_password and confirm_password:
                if new_password == confirm_password:
                    valid, message = Validators.validate_password(new_password)
                    if valid:
                        success = HealthData.update_password(
                            st.session_state.user['id'],
                            current_password,
                            new_password
                        )
                        if success:
                            st.markdown(
                                '<div class="success-message">Password updated successfully!</div>',
                                unsafe_allow_html=True
                            )
                            updates_made = True
                        else:
                            st.markdown(
                                '<div class="error-message">Current password is incorrect</div>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                            f'<div class="error-message">{message}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        '<div class="error-message">New passwords do not match</div>',
                        unsafe_allow_html=True
                    )
            
            # Handle MFA update
            current_mfa = current_user.get('mfa_enabled', False)
            if enable_mfa != current_mfa:
                success = HealthData.update_mfa_settings(
                    st.session_state.user['id'],
                    enable_mfa
                )
                if success:
                    st.markdown(
                        '<div class="success-message">MFA settings updated successfully!</div>',
                        unsafe_allow_html=True
                    )
                    updates_made = True
                else:
                    st.markdown(
                        '<div class="error-message">Failed to update MFA settings</div>',
                        unsafe_allow_html=True
                    )
            
            if updates_made:
                st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Notification Settings
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Notification Settings</h2>
    """, unsafe_allow_html=True)
    
    with st.form("notification_form"):
        email_notifications = st.checkbox(
            "Email Notifications",
            value=current_user.get('email_notifications', True)
        )
        
        st.write("Notification Preferences:")
        vital_alerts = st.checkbox(
            "Vital Signs Alerts",
            value=current_user.get('vital_alerts', True),
            help="Get alerts when vital signs are outside normal ranges"
        )
        
        med_reminders = st.checkbox(
            "Medication Reminders",
            value=current_user.get('med_reminders', True),
            help="Receive reminders to take your medications"
        )
        
        appointment_reminders = st.checkbox(
            "Appointment Reminders",
            value=current_user.get('appointment_reminders', True),
            help="Get reminders before scheduled appointments"
        )
        
        reminder_time = st.time_input(
            "Daily Reminder Time",
            value=current_user.get('reminder_time', None)
        )
        
        reminder_frequency = st.select_slider(
            "Reminder Frequency",
            options=["Low", "Medium", "High"],
            value=current_user.get('reminder_frequency', "Medium")
        )
        
        if st.form_submit_button("Update Notification Settings"):
            success = HealthData.update_notification_settings(
                st.session_state.user['id'],
                {
                    'email_notifications': email_notifications,
                    'vital_alerts': vital_alerts,
                    'med_reminders': med_reminders,
                    'appointment_reminders': appointment_reminders,
                    'reminder_time': reminder_time,
                    'reminder_frequency': reminder_frequency
                }
            )
            if success:
                st.markdown(
                    '<div class="success-message">Notification settings updated successfully!</div>',
                    unsafe_allow_html=True
                )
                st.rerun()
            else:
                st.markdown(
                    '<div class="error-message">Failed to update notification settings</div>',
                    unsafe_allow_html=True
                )
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Delete Account
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card danger-zone">
                <h2>Delete Account</h2>
                <div class="warning-text">⚠️ Warning: This action cannot be undone</div>
    """, unsafe_allow_html=True)
    
    with st.form("delete_account_form"):
        st.warning(
            "Account deletion is permanent. All your data will be erased."
        )
        
        confirm_delete = st.text_input(
            "Type 'DELETE' to confirm",
            help="This action is permanent and cannot be undone"
        )
        delete_password = st.text_input(
            "Enter your password",
            type="password"
        )
        
        if st.form_submit_button("Delete Account", type="primary"):
            if confirm_delete == "DELETE" and delete_password:
                success = HealthData.delete_user_account(
                    st.session_state.user['id'],
                    delete_password
                )
                if success:
                    st.markdown(
                        '<div class="success-message">Account deleted successfully.</div>',
                        unsafe_allow_html=True
                    )
                    st.session_state.clear()
                    st.rerun()
                else:
                    st.markdown(
                        '<div class="error-message">Failed to delete account. Please check your password.</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div class="error-message">Please type \'DELETE\' and enter your password to confirm.</div>',
                    unsafe_allow_html=True
                )
    
    st.markdown('</div></div>', unsafe_allow_html=True)