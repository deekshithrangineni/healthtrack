# frontend/styles/styles.py

def get_healthtrack_styles():
    return """
<style>
    /* Main Theme Colors */
    :root {
        --primary: #2196F3;
        --primary-dark: #1976D2;
        --primary-light: #BBDEFB;
        --accent: #FF4081;
        --background: #F5F7F9;
        --surface: #FFFFFF;
        --error: #B00020;
        --success: #4CAF50;
        --text-primary: #212121;
        --text-secondary: #757575;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background);
    }

    /* Navigation */
    .nav-header {
        padding: 1rem 0.5rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(49, 51, 63, 0.2);
    }

    .nav-header h2 {
        margin: 0;
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 600;
    }

    .stButton button {
        width: 100%;
        text-align: left;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0.5rem;
        border: none;
        background: transparent;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        background: rgba(151, 166, 195, 0.15);
        transform: translateX(4px);
    }

    /* User Menu */
    .user-menu {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 0.5rem 1rem;
        gap: 0.5rem;
        background: var(--surface);
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .user-name {
        font-weight: 500;
        color: var(--text-primary);
    }

    .user-menu-icon {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    /* Cards */
    .healthtrack-card {
        background: var(--surface);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .healthtrack-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Stats */
    .stat-card {
        background: var(--surface);
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary);
        margin: 0.5rem 0;
    }

    .stat-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }

    /* Messages */
    .success-message {
        background-color: var(--success);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    .error-message {
        background-color: var(--error);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }

    /* Forms */
    .form-container {
        background: var(--surface);
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Tables */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }

    .dataframe th {
        background: var(--primary-light);
        color: var(--text-primary);
        padding: 0.75rem;
        text-align: left;
    }

    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }

    /* Sidebar Footer */
    .sidebar-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 1rem;
        text-align: center;
        font-size: 0.75rem;
        color: var(--text-secondary);
        background: var(--background);
        border-top: 1px solid rgba(49, 51, 63, 0.2);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .healthtrack-card {
            padding: 1rem;
        }
        
        .stat-value {
            font-size: 1.5rem;
        }
        
        .user-menu {
            padding: 0.25rem 0.5rem;
        }
    }
</style>
"""