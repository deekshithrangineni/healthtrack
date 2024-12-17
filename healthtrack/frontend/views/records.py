# frontend/views/records.py
import streamlit as st
from backend.models import HealthData
from backend.security import Security

def render_records_view():
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h1>Medical Records</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Upload new record
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Upload Medical Record</h2>
    """, unsafe_allow_html=True)
    
    with st.form("record_upload_form"):
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "jpg", "jpeg", "png", "doc", "docx"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            record_type = st.selectbox("Record Type", [
                "Lab Report",
                "Imaging",
                "Prescription",
                "Visit Summary",
                "Vaccination Record",
                "Insurance",
                "Other"
            ])
        
        with col2:
            record_date = st.date_input("Record Date")
        
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Upload Record")
        
        if submitted and uploaded_file:
            try:
                filename, original_name = Security.save_file_securely(
                    uploaded_file,
                    st.session_state.user['id']
                )
                record = {
                    'title': original_name,
                    'record_type': record_type,
                    'record_date': record_date,
                    'file_path': filename,
                    'notes': notes
                }
                success = HealthData.add_medical_record(
                    st.session_state.user['id'],
                    record
                )
                if success:
                    st.markdown(
                        '<div class="success-message">Record uploaded successfully!</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div class="error-message">Failed to upload record</div>',
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.markdown(
                    f'<div class="error-message">Error uploading file: {str(e)}</div>',
                    unsafe_allow_html=True
                )
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Display records
    st.markdown("""
        <div class="container">
            <div class="healthtrack-card">
                <h2>Medical Records History</h2>
    """, unsafe_allow_html=True)
    
    record_filter = st.selectbox(
        "Filter by Type",
        ["All", "Lab Report", "Imaging", "Prescription", 
         "Visit Summary", "Vaccination Record", "Insurance", "Other"]
    )
    
    records = HealthData.get_medical_records(
        st.session_state.user['id'],
        record_type=record_filter
    )
    
    if records:
        for record in records:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">{record['record_type']}</div>
                    <div class="metric-value">{record['title']}</div>
                    <div class="metric-subtitle">Date: {record['record_date']}</div>
                    {f'<div class="metric-notes">{record["notes"]}</div>' if record['notes'] else ''}
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Download", key=f"dl_{record['id']}"):
                    try:
                        file_path = Security.get_file_path(
                            st.session_state.user['id'],
                            record['file_path']
                        )
                        with open(file_path, 'rb') as f:
                            st.download_button(
                                "Download File",
                                f,
                                file_name=record['title'],
                                mime="application/octet-stream"
                            )
                    except Exception as e:
                        st.markdown(
                            f'<div class="error-message">Error downloading file: {str(e)}</div>',
                            unsafe_allow_html=True
                        )
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="info-message">No records found.</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div></div>', unsafe_allow_html=True)