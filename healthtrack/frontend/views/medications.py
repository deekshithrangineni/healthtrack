# frontend/views/medications.py
import streamlit as st
from datetime import datetime
from backend.models import HealthData

def render_medications_view():
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h1>Medications Management</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add new medication
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Add New Medication</h2>
    """, unsafe_allow_html=True)
    
    with st.form("medication_form"):
        med_name = st.text_input("Medication Name")
        
        col1, col2 = st.columns(2)
        with col1:
            dosage = st.text_input("Dosage (e.g., 50mg)")
            frequency = st.selectbox("Frequency", [
                "Once daily",
                "Twice daily",
                "Three times daily",
                "Every 4 hours",
                "Every 6 hours",
                "Every 8 hours",
                "As needed"
            ])
        
        with col2:
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date (optional)")
        
        notes = st.text_area("Notes (optional)")
        
        submitted = st.form_submit_button("Add Medication")
        
        if submitted:
            if med_name and dosage:
                medication = {
                    'name': med_name,
                    'dosage': dosage,
                    'frequency': frequency,
                    'start_date': start_date,
                    'end_date': end_date if end_date > start_date else None,
                    'notes': notes,
                    'active': True
                }
                
                success = HealthData.add_medication(
                    st.session_state.user['id'], 
                    medication
                )
                if success:
                    st.markdown(
                        '<div class="success-message">Medication added successfully!</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div class="error-message">Failed to add medication</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div class="error-message">Please fill in required fields</div>',
                    unsafe_allow_html=True
                )
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Display current medications
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Current Medications</h2>
    """, unsafe_allow_html=True)
    
    show_inactive = st.checkbox("Show discontinued medications")
    
    medications = HealthData.get_medications(
        st.session_state.user['id'],
        active_only=not show_inactive
    )
    
    if medications:
        for med in medications:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">{med['frequency']}</div>
                    <div class="metric-value">{med['name']} - {med['dosage']}</div>
                    <div class="metric-subtitle">Started: {med['start_date']}</div>
                    {f'<div class="metric-subtitle">Ends: {med["end_date"]}</div>' if med['end_date'] else ''}
                    {f'<div class="metric-notes">{med["notes"]}</div>' if med['notes'] else ''}
            """, unsafe_allow_html=True)
            
            if med['active']:
                if st.button("Discontinue", key=f"disc_{med['id']}"):
                    if HealthData.update_medication_status(med['id'], False):
                        st.markdown(
                            '<div class="success-message">Medication discontinued</div>',
                            unsafe_allow_html=True
                        )
                        st.rerun()
            else:
                st.markdown(
                    '<div class="info-message">Status: Discontinued</div>',
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="info-message">No medications found.</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div></div>', unsafe_allow_html=True)