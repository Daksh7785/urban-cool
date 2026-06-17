import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Copilot from './pages/Copilot';
import InteractiveMap from './components/Map';
import { Activity, Map as MapIcon, Settings as SettingsIcon, User, Bot, Zap, Menu, X } from 'lucide-react';

function Navigation({ closeMenu }: { closeMenu: () => void }) {
  const location = useLocation();
  
  const getLinkClass = (path: string) => {
    const isActive = location.pathname === path;
    return `flex items-center space-x-3 p-3 rounded-lg transition ${isActive ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`;
  };

  return (
    <nav className="flex-1 p-4 space-y-2">
      <Link to="/" className={getLinkClass('/')} onClick={closeMenu}>
        <Activity size={20} />
        <span>Dashboard</span>
      </Link>
      <Link to="/map" className={getLinkClass('/map')} onClick={closeMenu}>
        <MapIcon size={20} />
        <span>Interactive GIS</span>
      </Link>
      <Link to="/copilot" className={getLinkClass('/copilot')} onClick={closeMenu}>
        <Bot size={20} />
        <span>AI Copilot</span>
      </Link>
      <Link to="/settings" className={getLinkClass('/settings')} onClick={closeMenu}>
        <SettingsIcon size={20} />
        <span>Settings</span>
      </Link>
    </nav>
  );
}

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [systemStatus, setSystemStatus] = useState('System Healthy');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleNewAnalysis = async () => {
    setIsAnalyzing(true);
    setSystemStatus('Running Analysis...');
    try {
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
      <div className="flex h-screen bg-slate-900 overflow-hidden">
        {/* Mobile Menu Overlay */}
        {isMobileMenuOpen && (
          <div 
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setIsMobileMenuOpen(false)}
          ></div>
        )}

        {/* Sidebar */}
        <aside className={`fixed lg:static inset-y-0 left-0 w-64 bg-slate-900 border-r border-slate-800 text-white flex flex-col z-50 transform transition-transform duration-300 ease-in-out ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
          <div className="p-4 text-2xl font-bold border-b border-slate-800 flex justify-between items-center">
            <div className="flex items-center">
              <span className="text-blue-400 mr-2 flex items-center justify-center bg-blue-500/10 rounded p-1">
                 <Activity size={24} className="animate-pulse text-blue-400"/>
              </span> 
              <span className="tracking-tight">CIOS AI</span>
            </div>
            <button className="lg:hidden text-slate-400 hover:text-white" onClick={() => setIsMobileMenuOpen(false)}>
              <X size={24} />
            </button>
          </div>
          <Navigation closeMenu={() => setIsMobileMenuOpen(false)} />
          <div className="p-4 border-t border-slate-800 flex items-center space-x-3 text-slate-300 hover:text-white cursor-pointer bg-slate-900 hover:bg-slate-800 transition-colors">
            <User size={20} />
            <span>Profile</span>
          </div>
        </aside>
        
        {/* Main Content */}
        <main className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden bg-slate-950 text-slate-200 relative">
          {/* Subtle global glow behind the content */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-blue-900/10 rounded-full blur-[120px] pointer-events-none"></div>

          <header className="bg-slate-900/80 backdrop-blur-md shadow-sm border-b border-slate-800 px-4 md:px-8 py-4 flex justify-between items-center z-10 sticky top-0">
            <div className="flex items-center gap-4">
              <button 
                className="lg:hidden text-slate-300 hover:text-white"
                onClick={() => setIsMobileMenuOpen(true)}
              >
                <Menu size={24} />
              </button>
              <h1 className="text-xl md:text-2xl font-bold text-slate-100 hidden sm:block">Global Command Center</h1>
            </div>
            
            <div className="flex space-x-3 md:space-x-4 items-center">
              <span className={`text-xs md:text-sm font-bold py-1.5 px-3 md:px-4 rounded-full border flex items-center gap-2 ${systemStatus.includes('Healthy') ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'}`}>
                <div className={`w-2 h-2 rounded-full ${systemStatus.includes('Healthy') ? 'bg-emerald-400 animate-pulse' : 'bg-yellow-400'}`}></div>
                <span className="hidden sm:inline">{systemStatus}</span>
                <span className="sm:hidden">Live</span>
              </span>
              <button 
                onClick={handleNewAnalysis}
                disabled={isAnalyzing}
                className="bg-blue-600/20 text-blue-400 border border-blue-500/30 px-3 md:px-5 py-2 rounded-lg text-xs md:text-sm font-bold hover:bg-blue-600/30 transition-all disabled:opacity-50 flex items-center space-x-2 shadow-[0_0_15px_rgba(37,99,235,0.2)] hover:shadow-[0_0_25px_rgba(37,99,235,0.4)]">
                <Zap size={16} className={isAnalyzing ? "animate-bounce" : ""} />
                <span className="hidden sm:inline">{isAnalyzing ? 'Processing Pipeline...' : 'ONE-CLICK OPTIMIZER'}</span>
                <span className="sm:hidden">Optimize</span>
              </button>
            </div>
          </header>
          
          <div className="flex-1 overflow-y-auto p-4 md:p-8 relative z-10 custom-scrollbar">
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
