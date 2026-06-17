import React from 'react';
// import Map, { Source, Layer } from 'react-map-gl';
// import 'mapbox-gl/dist/mapbox-gl.css';

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || '';

export default function LiveGlobeMap() {
  if (!MAPBOX_TOKEN) {
    return (
      <div className="w-full h-96 bg-slate-900 border border-slate-700 rounded-xl flex items-center justify-center text-slate-400">
        <p>Mapbox GL requires VITE_MAPBOX_TOKEN to render the 3D globe.</p>
      </div>
    );
  }

  return (
    <div className="w-full h-96 rounded-xl overflow-hidden border border-slate-700">
      {/* 
      <Map
        initialViewState={{
          longitude: 77.2090,
          latitude: 28.6139,
          zoom: 11
        }}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
        terrain={{source: 'mapbox-dem', exaggeration: 1.5}}
      >
        <Source id="mapbox-dem" type="raster-dem" url="mapbox://mapbox.mapbox-terrain-dem-v1" tileSize={512} maxzoom={14} />
      </Map>
      */}
    </div>
  );
}
