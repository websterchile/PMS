import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MaintenanceLog({ token }) {
  const [logs, setLogs] = useState([]);
  const [action, setAction] = useState('');
  const [pumpId, setPumpId] = useState('pump1');

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/logs/', {
          headers: { Authorization: `Bearer ${token}` },
          params: { pump_id: 'pump1' },
        });
        setLogs(response.data);
      } catch (error) {
        console.error('Error fetching maintenance logs:', error);
      }
    };
    fetchLogs();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        'http://localhost:8000/api/logs/',
        { action, pump_id: pumpId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const response = await axios.get('http://localhost:8000/api/logs/', {
        headers: { Authorization: `Bearer ${token}` },
        params: { pump_id: 'pump1' },
      });
      setLogs(response.data);
      setAction('');
    } catch (error) {
      console.error('Error adding maintenance log:', error);
    }
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-semibold text-primary mb-4">Maintenance Logs</h2>
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Action</label>
          <input
            type="text"
            value={action}
            onChange={(e) => setAction(e.target.value)}
            className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Enter maintenance action"
            required
          />
        </div>
        <button type="submit" className="btn-primary">Add Log</button>
      </form>
      <ul className="space-y-4">
        {logs.map(log => (
          <li key={log.log_id} className="p-4 bg-gray-50 rounded border">
            <p className="text-gray-800">{log.action}</p>
            <p className="text-sm text-gray-600">
              By {log.user} on {new Date(log.timestamp).toLocaleString()}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MaintenanceLog;