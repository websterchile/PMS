from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    vibration = models.FloatField()
    label = models.CharField(max_length=20)

class MaintenanceLog(models.Model):
    pump_id = models.CharField(max_length=32)
    action = models.CharField(max_length=128)
    performed_by = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pump_id} - {self.action} by {self.performed_by} at {self.timestamp}"
