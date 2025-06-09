from django import forms
from .models import MaintenanceLog

class MaintenanceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['pump_id', 'action', 'performed_by', 'notes']