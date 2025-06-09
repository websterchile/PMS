import pandas as pd
import numpy as np

n_samples = 1000
data = {
    "timestamp": pd.date_range("2025-06-01", periods=n_samples, freq="H"),
    "temperature": np.random.normal(70, 10, n_samples),
    "vibration": np.random.normal(5, 2, n_samples),
    "label": np.random.choice(["Normal", "Warning", "Critical"], n_samples, p=[0.7, 0.2, 0.1])
}
df = pd.DataFrame(data)
df.to_csv("simulated_sensor_data.csv", index=False)