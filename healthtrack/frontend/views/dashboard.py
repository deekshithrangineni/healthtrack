# frontend/views/dashboard.py
import streamlit as st
import pandas as pd
from backend.models import HealthData

def render_dashboard():
    st.title("Dashboard")
    
    # Recent Activity Section
    st.header("Recent Activity")
    
    tab1, tab2 = st.tabs(["Medical Records", "Medications"])
    
    with tab1:
        recent_records = HealthData.get_medical_records(
            user_id=st.session_state.user['id'],
            limit=5  # Get only last 5 records
        )
        if recent_records:
            for record in recent_records:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">{record['record_type']}</div>
                        <div class="metric-value">{record['title']}</div>
                        <div class="metric-date">{record['record_date']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent medical records")
            
    with tab2:
        recent_medications = HealthData.get_medications(
            user_id=st.session_state.user['id'],
            active_only=True,
            limit=5
        )
        if recent_medications:
            for med in recent_medications:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">{med['frequency']}</div>
                        <div class="metric-value">{med['name']} - {med['dosage']}</div>
                        <div class="metric-subtitle">Started: {med['start_date']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active medications")
    
    # Quick Stats Section
    st.header("Quick Stats")
    col1, col2, col3 = st.columns(3)
    
    # Get latest vitals
    latest_vitals = HealthData.get_vital_signs(st.session_state.user['id'], limit=1)
    
    if latest_vitals:
        vital = latest_vitals[0]
        
        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Blood Pressure</div>
                    <div class="stat-value">{vital['blood_pressure_sys']}/{vital['blood_pressure_dia']}</div>
                    <div class="stat-trend">Normal</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Heart Rate</div>
                    <div class="stat-value">{vital['heart_rate']} BPM</div>
                    <div class="stat-trend">Resting</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Weight</div>
                    <div class="stat-value">{vital['weight']} lbs</div>
                    <div class="stat-trend">Last Updated: {vital['date_recorded']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No vital signs recorded yet")
    
    # Health Trends
    st.header("Health Trends")
    trend_data = HealthData.get_vital_signs(
        st.session_state.user['id'],
        limit=30  # Last 30 days
    )
    
    if trend_data:
        df = pd.DataFrame(trend_data)
        df['date_recorded'] = pd.to_datetime(df['date_recorded'])
        
        # Blood Pressure Chart
        st.subheader("Blood Pressure (Last 30 Days)")
        bp_df = df[['date_recorded', 'blood_pressure_sys', 'blood_pressure_dia']]
        st.line_chart(bp_df.set_index('date_recorded'))
        
        # Heart Rate Chart
        st.subheader("Heart Rate Trends")
        hr_df = df[['date_recorded', 'heart_rate']]
        st.line_chart(hr_df.set_index('date_recorded'))
    else:
        st.info("No trend data available")