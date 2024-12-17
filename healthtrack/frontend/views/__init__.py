# frontend/views/__init__.py
from .auth import render_login
from .dashboard import render_dashboard
from .records import render_records_view
from .vitals import render_vitals_view
from .medications import render_medications_view
from .settings import render_settings_view

__all__ = [
    'render_login',
    'render_dashboard',
    'render_records_view',
    'render_vitals_view',
    'render_medications_view',
    'render_settings_view'
]