import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import axios from 'axios';

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);

  useEffect(() => {
    // 1. Fetch Prices
    axios.get('http://127.0.0.1:5000/api/prices')
      .then(res => setPrices(res.data.slice(-800)))
      .catch(err => console.error("Flask Prices API error:", err));

    // 2. Fetch Events
    axios.get('http://127.0.0.1:5000/api/events')
      .then(res => setEvents(res.data))
      .catch(err => console.error("Flask Events API error:", err));

    // 3. Fetch Change Point
    axios.get('http://127.0.0.1:5000/api/analysis-results')
      .then(res => setChangePoint(res.data.change_point_date))
      .catch(err => console.error("Flask Analysis API error:", err));
  }, []);

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f0f2f5', minHeight: '100vh' }}>
      <header style={{ marginBottom: '20px' }}>
        <h1 style={{ color: '#1a365d', margin: 0 }}>Birhan Energies: Brent Oil Dashboard</h1>
        <p style={{ color: '#4a5568' }}>Real-time Analysis & Change Point Detection</p>
      </header>
      
      <div style={{ display: 'grid', gridTemplateColumns: '3fr 1fr', gap: '20px' }}>
        {/* Chart Section */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginTop: 0 }}>Price Trend & Model Detection</h3>
          <div style={{ width: '100%', height: 450 }}>
            <ResponsiveContainer>
              <LineChart data={prices}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="Date" tick={{fontSize: 10}} minTickGap={100} />
                <YAxis domain={['auto', 'auto']} />
                <Tooltip />
                <Line type="monotone" dataKey="Price" stroke="#3182ce" strokeWidth={2} dot={false} />
                {changePoint && (
                  <ReferenceLine x={changePoint} stroke="red" strokeWidth={2} label={{ value: 'Change Point', position: 'top', fill: 'red', fontSize: 12 }} />
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Sidebar Section */}
        <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginTop: 0 }}>Key Geopolitical Events</h3>
          <div style={{ height: '450px', overflowY: 'auto', textAlign: 'left', paddingRight: '10px' }}>
            {events.length > 0 ? (
              events.map((e, i) => (
                <div key={i} style={{ borderBottom: '1px solid #edf2f7', padding: '12px 0' }}>
                  <div style={{ color: '#e53e3e', fontWeight: 'bold', fontSize: '11px', marginBottom: '4px' }}>
                    {e.Date || e.date}
                  </div>
                  <div style={{ fontSize: '13px', color: '#2d3748', lineHeight: '1.4' }}>
                    {e.Event || e.event || e.description || "Historical Event"}
                  </div>
                </div>
              ))
            ) : (
              <p style={{ color: '#a0aec0', fontSize: '14px' }}>Loading event data...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;