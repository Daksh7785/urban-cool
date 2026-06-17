import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Copilot from './pages/Copilot';
import InteractiveMap from './components/Map';
import { Activity, Map as MapIcon, Settings as SettingsIcon, User, Bot, Zap } from 'lucide-react';

function Navigation() {
  const location = useLocation();
  
  const getLinkClass = (path: string) => {
    const isActive = location.pathname === path;
    return `flex items-center space-x-3 p-3 rounded-lg transition ${isActive ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`;
  };

  return (
    <nav className="flex-1 p-4 space-y-2">
      <Link to="/" className={getLinkClass('/')}>
        <Activity size={20} />
        <span>Dashboard</span>
      </Link>
      <Link to="/map" className={getLinkClass('/map')}>
        <MapIcon size={20} />
        <span>Interactive GIS</span>
      </Link>
      <Link to="/copilot" className={getLinkClass('/copilot')}>
        <Bot size={20} />
        <span>AI Copilot</span>
      </Link>
      <Link to="/settings" className={getLinkClass('/settings')}>
        <SettingsIcon size={20} />
        <span>Settings</span>
      </Link>
    </nav>
  );
}

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [systemStatus, setSystemStatus] = useState('System Healthy');

  const handleNewAnalysis = async () => {
    setIsAnalyzing(true);
    setSystemStatus('Running Analysis...');
    try {
      // Try hitting the local backend if it's running
      const token = localStorage.getItem('token') || 'dummy-token';
      await axios.post('http://localhost:5000/api/analysis/run', {
        name: 'New Dashboard Request',
        city: 'Indore, India',
        bbox: '22.6, 75.8, 22.8, 76.0'
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSystemStatus('Analysis Queued');
    } catch (e) {
      // Fallback for Vercel demo mode
      console.log('Backend offline. Simulating analysis locally for demo...');
      setTimeout(() => {
        setSystemStatus('Demo Analysis Complete');
        setIsAnalyzing(false);
      }, 2000);
      return;
    }
    setIsAnalyzing(false);
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <aside className="w-64 bg-slate-900 text-white flex flex-col">
          <div className="p-4 text-2xl font-bold border-b border-slate-800 flex items-center">
            <span className="text-blue-400 mr-2">🌍</span> UrbanOS AI
          </div>
          <Navigation />
          <div className="p-4 border-t border-slate-800 flex items-center space-x-3 text-slate-300 hover:text-white cursor-pointer">
            <User size={20} />
            <span>Profile</span>
          </div>
        </aside>
        
        <main className="flex-1 overflow-y-auto">
          <header className="bg-white shadow-sm border-b px-8 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-slate-800">Global Command Center</h1>
            <div className="flex space-x-4 items-center">
              <span className={`text-sm font-medium py-1 px-3 rounded-full ${systemStatus.includes('Healthy') ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                {systemStatus}
              </span>
              <button 
                onClick={handleNewAnalysis}
                disabled={isAnalyzing}
                className="bg-slate-900 text-white px-4 py-2 rounded-md text-sm font-bold hover:bg-slate-800 transition disabled:opacity-50 flex items-center space-x-2">
                <Zap size={16} />
                <span>{isAnalyzing ? 'Processing...' : 'ONE-CLICK JUDGE DEMO'}</span>
              </button>
            </div>
          </header>
          
          <div className="p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/map" element={<InteractiveMap />} />
              <Route path="/copilot" element={<Copilot />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
