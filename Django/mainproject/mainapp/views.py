from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import pandas as pd
import numpy as np
from .models import MaintenanceLog
from .forms import MaintenanceLogForm
from datetime import datetime, timedelta
import json

def index(request):
    return render(request, 'index.html')

def sensors(request):
    return render(request, 'sensors.html')

def sensor_detail(request, sensor_type):
    df = pd.read_csv("mainapp/training/simulated_sensor_data.csv")
    sensor_data = df.head(10)
    return render(request, 'sensor_detail.html', {"sensor_type": sensor_type, "sensor_data": sensor_data})

def predictions(request):
    predictions = []
    df = pd.read_csv("mainapp/training/simulated_sensor_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Get the latest 10 readings for display
    latest_data = df.tail(10)

    # Build predictions per row
    for _, row in latest_data.iterrows():
        temp_status = "Normal" if row["temperature"] < 80 else "Warning" if row["temperature"] < 90 else "Critical"
        vib_status = "Normal" if row["vibration"] < 6 else "Warning" if row["vibration"] < 8 else "Critical"
        insight = []
        if temp_status != "Normal":
            insight.append(f"Temperature {temp_status}")
        if vib_status != "Normal":
            insight.append(f"Vibration {vib_status}")
        if not insight:
            insight.append("All sensors normal")
        predictions.append({
            "timestamp": row["timestamp"],
            "temperature": f"{row['temperature']:.2f}",
            "temperature_status": temp_status,
            "vibration": f"{row['vibration']:.2f}",
            "vibration_status": vib_status,
            "overall_status": row["label"],
            "insight": ", ".join(insight)
        })

    return render(
        request,
        "predictions.html",
        {
            "predictions": predictions[::-1],  # Show most recent first
        }
    )

def logs(request):
    logs = MaintenanceLog.objects.order_by('-timestamp')[:20]
    return render(request, 'logs.html', {'logs': logs})

def add_log(request):
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs')
    else:
        form = MaintenanceLogForm()
    return render(request, 'add_log.html', {'form': form})

def edit_log(request, log_id):
    log = get_object_or_404(MaintenanceLog, id=log_id)
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('logs')
    else:
        form = MaintenanceLogForm(instance=log)
    return render(request, 'add_log.html', {'form': form, 'edit': True})

def delete_log(request, log_id):
    log = get_object_or_404(MaintenanceLog, id=log_id)
    if request.method == 'POST':
        log.delete()
        return redirect('logs')
    return render(request, 'delete_log.html', {'log': log})

def maintenance(request):
    df = pd.read_csv("mainapp/training/simulated_sensor_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Check if sensors are reading data (simulate: if last value is recent)
    last_timestamp = df['timestamp'].max()
    now = pd.Timestamp.now()
    sensor_connected = (now - last_timestamp) < pd.Timedelta(hours=2)

    # Check if sensors are working (simulate: if last 3 readings are not all 'Critical')
    last_labels = df.tail(3)['label']
    all_critical = all(label == 'Critical' for label in last_labels)

    # Analyze the last 7 days
    last_week = df[df['timestamp'] >= (df['timestamp'].max() - pd.Timedelta(days=7))]
    warning_count = (last_week['label'] == 'Warning').sum()
    critical_count = (last_week['label'] == 'Critical').sum()

    # Maintenance due logic
    recent_issues = df[df['label'].isin(['Critical', 'Warning'])]
    if not recent_issues.empty:
        recent_issue = recent_issues.iloc[-1]
        maintenance_due = (recent_issue['timestamp'] + pd.Timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        due_soon = (pd.Timestamp(maintenance_due) - now).days <= 3
        health_status = recent_issue['label']
        health_score = 60 if health_status == "Warning" else 30
        alert = f"Alert: {recent_issue['label']} detected at {recent_issue['timestamp']}!"
    else:
        maintenance_due = (df['timestamp'].max() + pd.Timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        due_soon = False
        health_status = "Normal"
        health_score = 90
        alert = None

    # Dialogue messages
    dialogue = []
    if not sensor_connected:
        dialogue.append("Warning: Sensors are not connected or not sending data!")
    if all_critical:
        dialogue.append("Alert: All sensors are reporting CRITICAL status!")
    if due_soon:
        dialogue.append(f"Pump is due for maintenance by {maintenance_due}. Please schedule service.")
    if not dialogue:
        dialogue.append("All systems normal. No immediate maintenance required.")

    # Prepare data for charts (last 20 readings)
    chart_data = {
        "timestamps": [ts.strftime("%Y-%m-%d %H:%M") for ts in df.tail(20)['timestamp']],
        "temperature": list(df.tail(20)['temperature']),
        "vibration": list(df.tail(20)['vibration']),
    }

    return render(request, "maintenance.html", {
        "maintenance_due": maintenance_due,
        "sensor_connected": sensor_connected,
        "all_critical": all_critical,
        "dialogue": dialogue,
        "chart_data_json": json.dumps(chart_data),
        "health_status": health_status,
        "health_score": health_score,
        "warning_count": warning_count,
        "critical_count": critical_count,
        "alert": alert,
    })

def data_management(request):
    if request.method == "POST":
        if 'csv_upload' in request.FILES:
            csv_file = request.FILES['csv_upload']
            df = pd.read_csv(csv_file)
            # Save or process the uploaded CSV as needed
            messages.success(request, "CSV file uploaded successfully!")
        elif 'generate_synthetic' in request.POST:
            # Generate synthetic data (example: 10 rows)
            now = datetime.now()
            data = {
                "timestamp": [(now - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(10)],
                "temperature": np.random.normal(75, 10, 10),
                "vibration": np.random.normal(5, 2, 10),
                "label": np.random.choice(["Normal", "Warning", "Critical"], 10, p=[0.7, 0.2, 0.1])
            }
            df = pd.DataFrame(data)
            df.to_csv("mainapp/training/simulated_sensor_data.csv", index=False)
            messages.success(request, "Synthetic data generated and saved!")
        # logic for live data here

    return render(request, "data_management.html")

def help_page(request):
    return render(request, "help.html")
