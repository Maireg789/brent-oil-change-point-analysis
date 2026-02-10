import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import axios from 'axios';

const API_BASE = "http://127.0.0.1:5000/api";

function App() {
  const [allPrices, setAllPrices] = useState([]);
  const [displayPrices, setDisplayPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [filter, setFilter] = useState('All'); // 'All', '1Y', '5Y'

  useEffect(() => {
    axios.get(`${API_BASE}/prices`).then(res => {
      setAllPrices(res.data);
      setDisplayPrices(res.data.slice(-500)); // Default view
    });
    axios.get(`${API_BASE}/events`).then(res => setEvents(res.data));
    axios.get(`${API_BASE}/analysis-results`).then(res => setAnalysis(res.data));
  }, []);

  // Filter Logic: Addresses "Date Filters" feedback
  const handleFilter = (period) => {
    setFilter(period);
    if (period === '1Y') setDisplayPrices(allPrices.slice(-250));
    else if (period === '5Y') setDisplayPrices(allPrices.slice(-1250));
    else setDisplayPrices(allPrices.slice(-500));
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#f4f7f9', minHeight: '100vh', fontFamily: 'Inter, sans-serif' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ color: '#1a365d', borderBottom: '2px solid #3182ce', paddingBottom: '10px' }}>Birhan Energies | Oil Market Intelligence</h1>

        {/* Filter Controls */}
        <div style={{ margin: '20px 0', display: 'flex', gap: '10px' }}>
          {['1Y', '5Y', 'All'].map(p => (
            <button key={p} onClick={() => handleFilter(p)} 
              style={{ padding: '8px 20px', borderRadius: '5px', border: 'none', cursor: 'pointer',
              backgroundColor: filter === p ? '#3182ce' : '#cbd5e0', color: 'white' }}>{p}</button>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
          {/* Main Chart Section */}
          <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
            <h3>Historical Price Trend & Event Overlays</h3>
            <div style={{ width: '100%', height: 400 }}>
              <ResponsiveContainer>
                <LineChart data={displayPrices}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="Date" tick={{fontSize: 10}} minTickGap={100} />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="Price" stroke="#3182ce" dot={false} strokeWidth={2} />
                  {analysis && <ReferenceLine x={analysis.change_point_date} stroke="red" label="Model Break" />}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Key Insights Sidebar */}
          <div style={{ background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
            <h3>Quantified Analysis</h3>
            {analysis?.metrics && (
              <div style={{ background: '#ebf8ff', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
                <p><strong>Detected Change:</strong> {analysis.change_point_date}</p>
                <p><strong>Impact:</strong> {analysis.metrics.drop} Price Drop</p>
                <p style={{fontSize: '12px', color: '#4a5568'}}>{analysis.description}</p>
              </div>
            )}
            <h3>Event Timeline</h3>
            <div style={{ maxHeight: '250px', overflowY: 'auto', fontSize: '13px' }}>
              {events.map((e, i) => (
                <div key={i} style={{ padding: '8px 0', borderBottom: '1px solid #edf2f7' }}>
                  <span style={{ color: '#e53e3e', fontWeight: 'bold' }}>{e.Date}</span>: {e.Event}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;