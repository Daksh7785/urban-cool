import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Thermometer, Activity } from 'lucide-react';

// Fix for default marker icons in Leaflet with React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Global tracking coordinates to match the Dashboard
const initialGlobalHotspots = [
  { id: 1, lat: 28.6139, lng: 77.2090, temp: 47.2, intensity: 'Critical', name: 'New Delhi (Asia)' },
  { id: 2, lat: 33.4484, lng: -112.0740, temp: 45.8, intensity: 'Critical', name: 'Phoenix (N. America)' },
  { id: 3, lat: 30.0444, lng: 31.2357, temp: 44.1, intensity: 'High', name: 'Cairo (Africa)' },
  { id: 4, lat: 40.4168, lng: -3.7038, temp: 41.5, intensity: 'High', name: 'Madrid (Europe)' },
  { id: 5, lat: -37.8136, lng: 144.9631, temp: 39.8, intensity: 'Moderate', name: 'Melbourne (Oceania)' },
];

export default function InteractiveMap() {
  const [position, setPosition] = useState<[number, number]>([20.0, 0.0]); // Global center
  const [hotspots, setHotspots] = useState(initialGlobalHotspots);
  
  // Real-Time Simulator Effect for Map Geometries
  useEffect(() => {
    const interval = setInterval(() => {
      setHotspots(prev => prev.map(city => {
        const fluctuation = (Math.random() * 0.6 - 0.2).toFixed(1);
        const newTemp = Math.min(55, Math.max(30, city.temp + parseFloat(fluctuation)));
        
        let newIntensity = city.intensity;
        if (newTemp >= 45) newIntensity = 'Critical';
        else if (newTemp >= 41) newIntensity = 'High';
        else newIntensity = 'Moderate';

        return { ...city, temp: parseFloat(newTemp.toFixed(1)), intensity: newIntensity };
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);
  
  return (
    <div className="bg-slate-900 p-6 rounded-2xl shadow-2xl border border-slate-700 h-[750px] flex flex-col relative overflow-hidden">
      <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none z-0"></div>
      
      <div className="mb-6 flex justify-between items-center relative z-10">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="text-cyan-400 animate-pulse" />
            Global GIS Live Tracker
          </h2>
          <p className="text-slate-400 text-sm mt-1">Real-time satellite orbital mapping of thermal vulnerabilities.</p>
        </div>
        <div className="flex space-x-4 bg-slate-800 p-3 rounded-lg border border-slate-700">
          <span className="flex items-center text-sm font-semibold text-slate-300"><div className="w-3 h-3 rounded-full bg-red-500 mr-2 shadow-[0_0_10px_rgba(239,68,68,0.8)] animate-pulse"></div> Critical ({'>'}45°C)</span>
          <span className="flex items-center text-sm font-semibold text-slate-300"><div className="w-3 h-3 rounded-full bg-orange-500 mr-2 shadow-[0_0_10px_rgba(249,115,22,0.8)]"></div> High (41-45°C)</span>
          <span className="flex items-center text-sm font-semibold text-slate-300"><div className="w-3 h-3 rounded-full bg-yellow-400 mr-2 shadow-[0_0_10px_rgba(250,204,21,0.8)]"></div> Moderate ({'<'}41°C)</span>
        </div>
      </div>
      
      <div className="flex-1 rounded-xl overflow-hidden border-2 border-slate-700 shadow-inner relative z-10">
        <MapContainer center={position} zoom={3} style={{ height: '100%', width: '100%', backgroundColor: '#0f172a' }}>
          {/* Dark Mode CartoDB Voyager TileLayer */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          
          {hotspots.map(hotspot => {
            const color = hotspot.intensity === 'Critical' ? '#ef4444' : 
                          hotspot.intensity === 'High' ? '#f97316' : '#facc15';
            
            return (
              <React.Fragment key={hotspot.id}>
                <Circle 
                  center={[hotspot.lat, hotspot.lng]} 
                  pathOptions={{ 
                    color: color, 
                    fillColor: color, 
                    fillOpacity: 0.4,
                    weight: 2
                  }} 
                  radius={hotspot.temp * 15000} // Expanded radius for global scale visibility
                />
                <Marker position={[hotspot.lat, hotspot.lng]}>
                  <Popup className="custom-popup">
                    <div className="p-1">
                      <div className="font-bold text-slate-800 text-lg mb-1">{hotspot.name}</div>
                      <div className="flex items-center gap-1 text-red-600 font-black text-xl bg-red-50 p-2 rounded-md mb-2 border border-red-100">
                        <Thermometer size={18} />
                        {hotspot.temp.toFixed(1)}°C LST
                      </div>
                      <div className="text-sm font-semibold text-slate-600 mb-3 flex items-center gap-1">
                        <Activity size={14} /> Risk: <span style={{color}}>{hotspot.intensity}</span>
                      </div>
                      <button className="w-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold py-2 rounded shadow transition-colors">
                        INITIATE AI OPTIMIZER
                      </button>
                    </div>
                  </Popup>
                </Marker>
              </React.Fragment>
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
}
