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
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Mean City Temp" value="38.5°C" icon={<Thermometer className="text-orange-500" />} trend="+1.2°C" />
        <StatCard title="Detected Hotspots" value="14" icon={<AlertTriangle className="text-red-500" />} trend="2 new" />
        <StatCard title="Affected Population" value="1.2M" icon={<Users className="text-blue-500" />} trend="Stable" />
        <StatCard title="Active Interventions" value="6" icon={<Activity className="text-green-500" />} trend="+1" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <h2 className="text-lg font-semibold mb-4 text-slate-800">Top Hotspots by Temperature</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis unit="°C" />
                <Tooltip />
                <Bar dataKey="temp" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border">
          <h2 className="text-lg font-semibold mb-4 text-slate-800">Recent AI Analyses</h2>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                    <Activity size={18} />
                  </div>
                  <div>
                    <p className="font-medium text-slate-800">Indore Central District Analysis</p>
                    <p className="text-sm text-slate-500">2 hours ago • Automated Job</p>
                  </div>
                </div>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">Completed</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, trend }: { title: string, value: string, icon: React.ReactNode, trend: string }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border flex items-start justify-between">
      <div>
        <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-slate-800">{value}</h3>
        <p className="text-sm font-medium text-slate-400 mt-2">{trend}</p>
      </div>
      <div className="p-3 bg-slate-50 rounded-lg">
        {icon}
      </div>
    </div>
  );
}
