import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Alerts({ token }) {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/predictions/', {
          headers: { Authorization: `Bearer ${token}` },
          params: { pump_id: 'pump1' },
        });
        const predictions = response.data;
        const newAlerts = predictions
          .filter(pred => pred.failure_probability > 0.7)
          .map(pred => ({
            id: pred.prediction_id,
            message: `High failure risk on ${pred.pump_id}: ${pred.failure_probability * 100}%`,
            time_to_failure: pred.time_to_failure,
          }));
        setAlerts(newAlerts);
      } catch (error) {
        console.error('Error fetching alerts:', error);
      }
    };
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 60000);
    return () => clearInterval(interval);
  }, [token]);

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold text-primary mb-4">Alerts</h2>
      {alerts.length === 0 ? (
        <p className="text-gray-600">No alerts at this time.</p>
      ) : (
        <ul className="space-y-4">
          {alerts.map(alert => (
            <li key={alert.id} className="p-4 bg-danger/10 border-l-4 border-danger rounded">
              <p className="text-danger font-medium">{alert.message}</p>
              <p className="text-sm text-gray-600">
                Estimated time to failure: {alert.time_to_failure} hours
              </p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Alerts;