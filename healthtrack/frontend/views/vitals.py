# frontend/views/vitals.py
import streamlit as st
import pandas as pd
from backend.models import HealthData
from backend.validators import Validators

def render_vitals_view():
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h1>Vital Signs Management</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Input form for new vital signs
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Record New Vital Signs</h2>
    """, unsafe_allow_html=True)
    
    with st.form("vital_signs_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            blood_pressure_sys = st.number_input(
                "Blood Pressure (Systolic)", 70, 200, 120)
            blood_pressure_dia = st.number_input(
                "Blood Pressure (Diastolic)", 40, 130, 80)
        
        with col2:
            heart_rate = st.number_input("Heart Rate (BPM)", 40, 200, 75)
            temperature = st.number_input(
                "Temperature (°F)", 95.0, 105.0, 98.6)
        
        with col3:
            weight = st.number_input("Weight (lbs)", 50, 500, 150)
            oxygen = st.number_input("Oxygen Saturation (%)", 50, 100, 98)
        
        submitted = st.form_submit_button("Record Vital Signs")
        
        if submitted:
            vitals = {
                'blood_pressure_sys': blood_pressure_sys,
                'blood_pressure_dia': blood_pressure_dia,
                'heart_rate': heart_rate,
                'temperature': temperature,
                'weight': weight,
                'oxygen': oxygen
            }
            
            valid, message = Validators.validate_vital_signs(vitals)
            if valid:
                success, msg = HealthData.add_vital_signs(
                    st.session_state.user['id'], vitals)
                if success:
                    st.markdown(f'<div class="success-message">{msg}</div>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-message">{msg}</div>', 
                              unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-message">{message}</div>', 
                          unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # History Tabs
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Vital Signs History</h2>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Table View", "Chart View"])
    
    vitals = HealthData.get_vital_signs(st.session_state.user['id'])
    
    with tab1:
        if vitals:
            df = pd.DataFrame(vitals)
            df['date_recorded'] = pd.to_datetime(df['date_recorded'])
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download History (CSV)",
                data=csv,
                file_name="vital_signs_history.csv",
                mime="text/csv"
            )
        else:
            st.markdown('<div class="info-message">No vital signs recorded yet.</div>', 
                       unsafe_allow_html=True)
    
    with tab2:
        if vitals:
            df = pd.DataFrame(vitals)
            df['date_recorded'] = pd.to_datetime(df['date_recorded'])
            
            # Blood Pressure Chart
            st.subheader("Blood Pressure Trends")
            bp_df = df[['date_recorded', 'blood_pressure_sys', 'blood_pressure_dia']]
            st.line_chart(bp_df.set_index('date_recorded'))
            
            # Heart Rate Chart
            st.subheader("Heart Rate Trends")
            hr_df = df[['date_recorded', 'heart_rate']]
            st.line_chart(hr_df.set_index('date_recorded'))
            
            # Weight Chart
            st.subheader("Weight Trends")
            weight_df = df[['date_recorded', 'weight']]
            st.line_chart(weight_df.set_index('date_recorded'))
        else:
            st.markdown('<div class="info-message">No data available for charts.</div>', 
                       unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)