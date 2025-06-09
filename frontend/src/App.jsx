import React, { useState } from 'react';
import SensorDataChart from './SensorDataChart.jsx';
import Alerts from './Alerts.jsx';
import MaintenanceLog from './MaintenanceLog.jsx';
import Login from './Login.jsx';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div className="min-h-screen bg-background font-sans p-6">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-primary text-center">Predictive Maintenance Dashboard</h1>
      </header>
      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <SensorDataChart token={token} />
        </div>
        <div className="space-y-6">
          <Alerts token={token} />
          <MaintenanceLog token={token} />
        </div>
      </main>
    </div>
  );
}

export default App;