import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Mock hotspot data for Indore (approximate coordinates)
const mockHotspots = [
  { id: 1, lat: 22.7196, lng: 75.8577, temp: 42, intensity: 'High', name: 'Rajwada Area' },
  { id: 2, lat: 22.7533, lng: 75.8937, temp: 45, intensity: 'Critical', name: 'Vijay Nagar' },
  { id: 3, lat: 22.6869, lng: 75.8324, temp: 39, intensity: 'Medium', name: 'Bhawarkuan' },
  { id: 4, lat: 22.7244, lng: 75.8839, temp: 41, intensity: 'High', name: 'Palasia' },
];

export default function InteractiveMap() {
  const [position, setPosition] = useState<[number, number]>([22.7196, 75.8577]); // Default to Indore
  
  return (
    <div className="bg-white p-4 rounded-xl shadow-sm border h-[700px] flex flex-col">
      <div className="mb-4 flex justify-between items-center">
        <h2 className="text-xl font-semibold text-slate-800">Interactive Urban Heat Island Map</h2>
        <div className="flex space-x-2">
          <span className="flex items-center text-sm"><div className="w-3 h-3 rounded-full bg-red-600 mr-2 opacity-50"></div> Critical</span>
          <span className="flex items-center text-sm"><div className="w-3 h-3 rounded-full bg-orange-500 mr-2 opacity-50"></div> High</span>
          <span className="flex items-center text-sm"><div className="w-3 h-3 rounded-full bg-yellow-400 mr-2 opacity-50"></div> Medium</span>
        </div>
      </div>
      
      <div className="flex-1 rounded-lg overflow-hidden border border-slate-200 relative z-0">
        <MapContainer center={position} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {mockHotspots.map(hotspot => {
            const color = hotspot.intensity === 'Critical' ? '#dc2626' : 
                          hotspot.intensity === 'High' ? '#f97316' : '#facc15';
            
            return (
              <React.Fragment key={hotspot.id}>
                <Circle 
                  center={[hotspot.lat, hotspot.lng]} 
                  pathOptions={{ color, fillColor: color, fillOpacity: 0.5 }} 
                  radius={hotspot.temp * 20} 
                />
                <Marker position={[hotspot.lat, hotspot.lng]}>
                  <Popup>
                    <div className="font-semibold">{hotspot.name}</div>
                    <div className="text-red-600 font-bold">{hotspot.temp}°C LST</div>
                    <div className="text-sm text-slate-600">Intensity: {hotspot.intensity}</div>
                    <button className="mt-2 w-full bg-blue-600 text-white text-xs py-1 rounded">View Details</button>
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
