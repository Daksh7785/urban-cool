import React, { useState } from 'react';
import { Save, Bell, Shield, Database, User } from 'lucide-react';

export default function Settings() {
  const [activeTab, setActiveTab] = useState('general');

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden flex h-[700px]">
      {/* Sidebar */}
      <div className="w-64 bg-slate-50 border-r border-slate-200 p-4">
        <h2 className="text-lg font-bold text-slate-800 mb-4 px-2">Settings</h2>
        <nav className="space-y-1">
          <button 
            onClick={() => setActiveTab('general')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium ${activeTab === 'general' ? 'bg-blue-100 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            <User size={18} />
            <span>General</span>
          </button>
          <button 
            onClick={() => setActiveTab('notifications')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium ${activeTab === 'notifications' ? 'bg-blue-100 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            <Bell size={18} />
            <span>Notifications</span>
          </button>
          <button 
            onClick={() => setActiveTab('data')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium ${activeTab === 'data' ? 'bg-blue-100 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            <Database size={18} />
            <span>Data Sources</span>
          </button>
          <button 
            onClick={() => setActiveTab('security')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium ${activeTab === 'security' ? 'bg-blue-100 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            <Shield size={18} />
            <span>Security</span>
          </button>
        </nav>
      </div>

      {/* Content */}
      <div className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-2xl">
          <h1 className="text-2xl font-bold text-slate-900 mb-6 capitalize">{activeTab} Settings</h1>
          
          {activeTab === 'general' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Project Name</label>
                <input type="text" defaultValue="UrbanCool Main Initiative" className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Default City</label>
                <input type="text" defaultValue="Indore, India" className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Analysis Frequency</label>
                <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Daily</option>
                  <option>Weekly</option>
                  <option>Monthly</option>
                  <option>Manual Only</option>
                </select>
              </div>
              <button className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition">
                <Save size={18} />
                <span>Save Changes</span>
              </button>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-4">
              <label className="flex items-center space-x-3">
                <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 rounded border-slate-300" />
                <span className="text-slate-700">Email me when a new hotspot is detected</span>
              </label>
              <label className="flex items-center space-x-3">
                <input type="checkbox" defaultChecked className="h-4 w-4 text-blue-600 rounded border-slate-300" />
                <span className="text-slate-700">Send weekly summary reports</span>
              </label>
              <label className="flex items-center space-x-3">
                <input type="checkbox" className="h-4 w-4 text-blue-600 rounded border-slate-300" />
                <span className="text-slate-700">Notify on analysis failures</span>
              </label>
            </div>
          )}
          
          {activeTab === 'data' && (
            <div className="space-y-6">
              <div className="p-4 border border-blue-100 bg-blue-50 rounded-lg">
                <h3 className="font-medium text-blue-800 mb-2">Google Earth Engine API</h3>
                <p className="text-sm text-blue-600 mb-3">Status: Connected</p>
                <button className="bg-white border border-blue-200 text-blue-700 px-3 py-1 rounded text-sm font-medium">Configure</button>
              </div>
              <div className="p-4 border border-slate-200 rounded-lg">
                <h3 className="font-medium text-slate-800 mb-2">OpenStreetMap Database</h3>
                <p className="text-sm text-slate-500 mb-3">Status: Local Cache Valid</p>
                <button className="bg-white border border-slate-200 text-slate-700 px-3 py-1 rounded text-sm font-medium">Force Sync</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
