import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import axios from 'axios';

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);

  useEffect(() => {
    // 1. Fetch Prices from your Flask API
    axios.get('http://127.0.0.1:5000/api/prices')
      .then(res => setPrices(res.data.slice(-800))) // Show last 800 entries for better performance
      .catch(err => console.log("Backend not running?"));

    // 2. Fetch the detected Change Point
    axios.get('http://127.0.0.1:5000/api/analysis-results')
      .then(res => setChangePoint(res.data.change_point_date));

    // 3. Fetch the Events list
    axios.get('http://127.0.0.1:5000/api/events')
      .then(res => setEvents(res.data));
  }, []);

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <h1 style={{ color: '#2c3e50' }}>Birhan Energies: Brent Oil Insights</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '3fr 1fr', gap: '20px' }}>
        {/* Main Chart Section */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <h3>Historical Price Trend & Change Point</h3>
          <div style={{ width: '100%', height: 400 }}>
            <ResponsiveContainer>
              <LineChart data={prices}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="Date" tick={{fontSize: 10}} minTickGap={100} />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="Price" stroke="#3498db" dot={false} strokeWidth={2} />
                {changePoint && (
                  <ReferenceLine x={changePoint} stroke="red" strokeDasharray="3 3" label={{ value: 'Change Point', position: 'top', fill: 'red' }} />
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Events Sidebar */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <h3>Key Events</h3>
          <div style={{ height: '400px', overflowY: 'auto' }}>
            {events.length > 0 ? events.map((e, i) => (
  <div key={i} style={{ borderBottom: '1px solid #eee', padding: '10px 0' }}>
    <small style={{ color: '#e74c3c', fontWeight: 'bold' }}>{e.Date || e.date}</small>
    <p style={{ margin: '5px 0', fontSize: '13px' }}>
      {e.Event || e.event || e.description || "No description"}
    </p>
  </div>
)) : <p>Loading events from CSV...</p>}