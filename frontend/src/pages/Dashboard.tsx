import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Thermometer, Users, AlertTriangle, Activity, Globe } from 'lucide-react';

const initialGlobalData = [
  { name: 'New Delhi', temp: 47.2, pop: 32000000, risk: 'Critical' },
  { name: 'Phoenix', temp: 45.8, pop: 1600000, risk: 'Critical' },
  { name: 'Cairo', temp: 44.1, pop: 22000000, risk: 'High' },
  { name: 'Madrid', temp: 41.5, pop: 3200000, risk: 'High' },
  { name: 'Melbourne', temp: 39.8, pop: 5000000, risk: 'Moderate' },
];

const initialAlerts = [
  { title: "New Delhi Heatwave Early Warning", time: "Just now", status: "Critical", type: "scan" },
  { title: "Phoenix Asphalt Cool Coating", time: "2 mins ago", status: "Optimized", type: "cooling" },
  { title: "Cairo Population Risk Assessment", time: "15 mins ago", status: "Completed", type: "budget" }
];

export default function Dashboard() {
  const [globalData, setGlobalData] = useState(initialGlobalData);
  const [alerts, setAlerts] = useState(initialAlerts);
  const [flash, setFlash] = useState(false);

  // Real-Time Simulator Effect
  useEffect(() => {
    const interval = setInterval(() => {
      // Stochastically alter temperatures to simulate live satellite stream
      setGlobalData(prev => prev.map(city => {
        const fluctuation = (Math.random() * 0.4 - 0.1).toFixed(1); // Tendency to heat up slightly
        const newTemp = Math.min(55, Math.max(30, city.temp + parseFloat(fluctuation)));
        return { ...city, temp: parseFloat(newTemp.toFixed(1)) };
      }).sort((a, b) => b.temp - a.temp)); // Sort hottest first

      // 10% chance to trigger a new AI alert
      if (Math.random() > 0.9) {
        setFlash(true);
        setTimeout(() => setFlash(false), 1000);
        
        const newCities = ['Dubai', 'Las Vegas', 'Baghdad', 'Seville'];
        const randomCity = newCities[Math.floor(Math.random() * newCities.length)];
        
        setAlerts(prev => [
          { title: `${randomCity} Thermal Anomaly Spike Detected`, time: "Just now", status: "Critical", type: "scan" },
          ...prev.slice(0, 3)
        ]);
      }
    }, 2500); // Update every 2.5 seconds

    return () => clearInterval(interval);
  }, []);

  const highestTemp = globalData[0].temp;
  const totalPop = (globalData.reduce((acc, curr) => acc + curr.pop, 0) / 1000000).toFixed(1);

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className={`relative overflow-hidden rounded-2xl p-8 border shadow-2xl transition-all duration-500 ${flash ? 'bg-red-900 border-red-500 shadow-[0_0_50px_rgba(239,68,68,0.4)]' : 'bg-gradient-to-br from-slate-900 via-slate-800 to-orange-950 border-slate-700'}`}>
        <div className="relative z-10">
          <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500 mb-2 flex items-center gap-3">
            <Globe className="text-orange-500" size={32} />
            Global Climate Intelligence Center
          </h2>
          <p className="text-slate-300 max-w-2xl mb-6 text-sm leading-relaxed">
            Live satellite feeds are actively monitoring global thermal anomalies. Real-time stochiastic engine engaged. AI Agents are currently routing cooling interventions to critical population centers.
          </p>
          <div className="flex space-x-4">
            <div className="flex items-center space-x-2 bg-red-500/10 border border-red-500/20 px-3 py-1.5 rounded-full text-red-400 text-xs font-semibold tracking-wide">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              <span>Live Satellite Stream ACTIVE</span>
            </div>
            <div className="flex items-center space-x-2 bg-cyan-500/10 border border-cyan-500/20 px-3 py-1.5 rounded-full text-cyan-400 text-xs font-semibold tracking-wide">
              <Activity size={14} className="text-cyan-400 animate-pulse" />
              <span>Multi-Agent Orchestrator Running</span>
            </div>
          </div>
        </div>
        
        {/* Abstract Background Element */}
        <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl pointer-events-none"></div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Peak Global Temp" value={`${highestTemp}°C`} icon={<Thermometer className="text-orange-500" />} trend="Live Tracking" color="orange" />
        <StatCard title="Monitored Cities" value="5" icon={<Globe className="text-blue-500" />} trend="Global Scale" color="blue" />
        <StatCard title="Tracked Population" value={`${totalPop}M`} icon={<Users className="text-purple-400" />} trend="High Vulnerability" color="purple" />
        <StatCard title="Live Interventions" value="12" icon={<Activity className="text-cyan-400" />} trend="Calculating ROI" color="cyan" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 shadow-xl backdrop-blur-sm transition-all duration-300">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
               <Thermometer size={18} className="text-orange-500 animate-pulse"/>
               Live Global Hotspots
            </h2>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={globalData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{fill: '#94a3b8'}} axisLine={false} tickLine={false} />
                <YAxis domain={[30, 55]} unit="°C" stroke="#94a3b8" tick={{fill: '#94a3b8'}} axisLine={false} tickLine={false} />
                <Tooltip 
                  cursor={{fill: '#1e293b'}}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc', borderRadius: '8px' }}
                  itemStyle={{ color: '#f97316' }}
                />
                <Bar dataKey="temp" fill="url(#heatGradient)" radius={[4, 4, 0, 0]} isAnimationActive={false} />
                <defs>
                  <linearGradient id="heatGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#ef4444" />
                    <stop offset="100%" stopColor="#f97316" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 shadow-xl backdrop-blur-sm">
          <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-2">
            <Activity size={18} className="text-cyan-400 animate-spin-slow" />
            Live Agent Ecosystem Feed
          </h2>
          <div className="space-y-4">
            {alerts.map((item, i) => (
              <div key={i} className={`flex items-center justify-between p-4 bg-slate-800 rounded-xl border hover:border-slate-600 transition group ${i === 0 ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'border-slate-700'}`}>
                <div className="flex items-center space-x-4">
                  <div className={`h-10 w-10 rounded-lg flex items-center justify-center ${item.type === 'cooling' ? 'bg-cyan-500/20 text-cyan-400' : item.type === 'scan' ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                    <Activity size={18} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-200 group-hover:text-white transition">{item.title}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{item.time} • AI Agent Orchestrator</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wide ${item.status === 'Critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20 animate-pulse' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'}`}>
                  {item.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, trend, color }: { title: string, value: string, icon: React.ReactNode, trend: string, color: string }) {
  const getGlow = () => {
    if(color === 'orange') return 'group-hover:shadow-[0_0_20px_rgba(249,115,22,0.3)]';
    if(color === 'red') return 'group-hover:shadow-[0_0_20px_rgba(239,68,68,0.3)]';
    if(color === 'purple') return 'group-hover:shadow-[0_0_20px_rgba(168,85,247,0.3)]';
    if(color === 'blue') return 'group-hover:shadow-[0_0_20px_rgba(59,130,246,0.3)]';
    return 'group-hover:shadow-[0_0_20px_rgba(34,211,238,0.3)]';
  };

  return (
    <div className={`bg-slate-800/50 p-6 rounded-2xl border border-slate-700 flex items-start justify-between relative overflow-hidden transition-all duration-300 group ${getGlow()}`}>
      <div className="relative z-10">
        <p className="text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wider">{title}</p>
        <h3 className="text-3xl font-black text-slate-100">{value}</h3>
        <p className={`text-sm font-bold mt-2 ${trend.includes('Critical') || trend.includes('High') ? 'text-red-400' : 'text-emerald-400'}`}>
          {trend}
        </p>
      </div>
      <div className="p-3 bg-slate-900/50 rounded-xl relative z-10 border border-slate-700/50">
        {icon}
      </div>
      
      {/* Subtle background glow */}
      <div className="absolute -bottom-10 -right-10 w-32 h-32 bg-slate-700/20 rounded-full blur-2xl group-hover:bg-slate-600/30 transition-colors"></div>
    </div>
  );
}
