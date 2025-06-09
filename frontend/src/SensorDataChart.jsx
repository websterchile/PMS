import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';
Chart.register(...registerables);

function SensorDataChart({ token }) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Temperature (°C)',
        data: [],
        borderColor: '#1E3A8A',
        fill: false,
      },
      {
        label: 'Vibration (m/s²)',
        data: [],
        borderColor: '#F59E0B',
        fill: false,
      },
    ],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/sensors/', {
          headers: { Authorization: `Bearer ${token}` },
          params: { pump_id: 'pump1', time_range: '1h' },
        });
        const data = response.data;
        setChartData({
          labels: data.map(d => new Date(d.timestamp)),
          datasets: [
            {
              label: 'Temperature (°C)',
              data: data.map(d => d.temperature),
              borderColor: '#1E3A8A',
              fill: false,
            },
            {
              label: 'Vibration (m/s²)',
              data: data.map(d => d.vibration),
              borderColor: '#F59E0B',
              fill: false,
            },
          ],
        });
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, [token]);

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold text-primary mb-4">Sensor Data Over Time</h2>
      <Line
        data={chartData}
        options={{
          responsive: true,
          scales: {
            x: { type: 'time', time: { unit: 'minute' } },
            y: { beginAtZero: true },
          },
        }}
      />
    </div>
  );
}

export default SensorDataChart;