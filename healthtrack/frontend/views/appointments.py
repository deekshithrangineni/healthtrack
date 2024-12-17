import streamlit as st
from datetime import datetime
from backend.models import HealthData

def render_appointments():
    st.title("Appointments")
    
    # Add Appointment button
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("+ Add Appointment"):
            st.session_state.subview = "add_appointment"
    
    if st.session_state.get('subview') == "add_appointment":
        render_add_appointment()
    else:
        render_appointments_list()

def render_add_appointment():
    st.subheader("Schedule New Appointment")
    
    with st.form("add_appointment_form"):
        title = st.text_input("Appointment Title")
        provider = st.text_input("Provider Name")
        
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date")
            time = st.time_input("Time")
        
        with col2:
            location = st.text_input("Location")
            
        notes = st.text_area("Notes")
        
        if st.form_submit_button("Schedule Appointment"):
            if title and provider and date and time:
                success, message = HealthData.add_appointment(st.session_state.user['id'], {
                    'title': title,
                    'provider': provider,
                    'appointment_date': date.strftime('%Y-%m-%d'),
                    'appointment_time': time.strftime('%H:%M'),
                    'location': location,
                    'notes': notes
                })
                if success:
                    st.success(message)
                    st.session_state.subview = None
                else:
                    st.error(message)
            else:
                st.error("Please fill in all required fields")

def render_appointments_list():
    appointments = HealthData.get_appointments(st.session_state.user['id'])
    
    for appt in appointments:
        with st.container():
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                st.markdown(f"### {appt['title']}")
                st.text(f"Provider: {appt['provider']}")
            with col2:
                st.text(f"Date: {appt['appointment_date']}")
                st.text(f"Time: {appt['appointment_time']}")
                if appt['location']:
                    st.text(f"Location: {appt['location']}")
            with col3:
                st.button("Cancel", key=f"cancel_appt_{appt['id']}")