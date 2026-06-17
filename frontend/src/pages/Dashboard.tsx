import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Thermometer, Users, AlertTriangle, Activity } from 'lucide-react';

const mockData = [
  { name: 'Hotspot 1', temp: 42, pop: 12000 },
  { name: 'Hotspot 2', temp: 45, pop: 8500 },
  { name: 'Hotspot 3', temp: 39, pop: 22000 },
  { name: 'Hotspot 4', temp: 48, pop: 5400 },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-slate-800 to-orange-950 p-8 border border-slate-700 shadow-2xl">
        <div className="relative z-10">
          <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500 mb-2">
            Urban Heat Mitigation Center
          </h2>
          <p className="text-slate-300 max-w-2xl mb-6 text-sm leading-relaxed">
            AI-driven spatial analytics are currently identifying extreme thermal anomalies. Our physics-informed engines are processing surface energy balances to recommend optimal cooling interventions.
          </p>
          <div className="flex space-x-4">
            <div className="flex items-center space-x-2 bg-red-500/10 border border-red-500/20 px-3 py-1.5 rounded-full text-red-400 text-xs font-semibold tracking-wide">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              <span>Thermal Anomalies Detected</span>
            </div>
            <div className="flex items-center space-x-2 bg-cyan-500/10 border border-cyan-500/20 px-3 py-1.5 rounded-full text-cyan-400 text-xs font-semibold tracking-wide">
              <Activity size={14} className="text-cyan-400" />
              <span>Optimizer Running</span>
            </div>
          </div>
        </div>
        
        {/* Abstract Background Element */}
        <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl pointer-events-none"></div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Mean City Temp" value="38.5°C" icon={<Thermometer className="text-orange-500" />} trend="+1.2°C" color="orange" />
        <StatCard title="Critical Hotspots" value="14" icon={<AlertTriangle className="text-red-500" />} trend="2 new" color="red" />
        <StatCard title="Vulnerable Population" value="1.2M" icon={<Users className="text-purple-400" />} trend="High Risk" color="purple" />
        <StatCard title="Active Cooling Projects" value="6" icon={<Activity className="text-cyan-400" />} trend="+1" color="cyan" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 shadow-xl backdrop-blur-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
               <Thermometer size={18} className="text-orange-500"/>
               Top Hotspots by Peak LST
            </h2>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{fill: '#94a3b8'}} axisLine={false} tickLine={false} />
                <YAxis unit="°C" stroke="#94a3b8" tick={{fill: '#94a3b8'}} axisLine={false} tickLine={false} />
                <Tooltip 
                  cursor={{fill: '#1e293b'}}
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc', borderRadius: '8px' }}
                  itemStyle={{ color: '#f97316' }}
                />
                <Bar dataKey="temp" fill="url(#heatGradient)" radius={[4, 4, 0, 0]} />
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
            <Activity size={18} className="text-cyan-400" />
            Recent AI Interventions
          </h2>
          <div className="space-y-4">
            {[
              { title: "Indore Central Cool Roofs", time: "2 hours ago", status: "Optimized", type: "cooling" },
              { title: "Zone B Heat Vulnerability Scan", time: "5 hours ago", status: "Critical", type: "scan" },
              { title: "Pareto Budget Balancer", time: "1 day ago", status: "Completed", type: "budget" }
            ].map((item, i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-slate-800 rounded-xl border border-slate-700 hover:border-slate-600 transition group">
                <div className="flex items-center space-x-4">
                  <div className={`h-10 w-10 rounded-lg flex items-center justify-center ${item.type === 'cooling' ? 'bg-cyan-500/20 text-cyan-400' : item.type === 'scan' ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                    <Activity size={18} />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-200 group-hover:text-white transition">{item.title}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{item.time} • AI Copilot</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wide ${item.status === 'Critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'}`}>
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
    return 'group-hover:shadow-[0_0_20px_rgba(34,211,238,0.3)]';
  };

  return (
    <div className={`bg-slate-800/50 p-6 rounded-2xl border border-slate-700 flex items-start justify-between relative overflow-hidden transition-all duration-300 group ${getGlow()}`}>
      <div className="relative z-10">
        <p className="text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wider">{title}</p>
        <h3 className="text-3xl font-black text-slate-100">{value}</h3>
        <p className={`text-sm font-bold mt-2 ${trend.includes('+') || trend.includes('High') ? 'text-red-400' : 'text-emerald-400'}`}>
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
