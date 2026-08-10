'use client';

import { useEffect, useRef } from 'react';

// Centro aproximado de Lalín (ajusta a tu zona)
const CENTRO = [42.6614, -8.1132];

export default function MapaValvulas() {
  const containerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    let map;
    let routingControl;
    let userMarker;
    let posOperario = null;

    (async () => {
      const L = (await import('leaflet')).default;
      await import('leaflet/dist/leaflet.css');
      // leaflet-routing-machine necesita L en global antes de importarse
      if (typeof window !== 'undefined') window.L = L;
      await import('leaflet-routing-machine');
      await import('leaflet-routing-machine/dist/leaflet-routing-machine.css');

      // Arreglo de iconos por defecto rotos en bundlers
      delete L.Icon.Default.prototype._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      });

      map = L.map(containerRef.current).setView(CENTRO, 15);
      mapRef.current = map;

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
        maxZoom: 19,
      }).addTo(map);

      // Icono de válvula
      const valveIcon = L.divIcon({
        className: 'valve-icon',
        html: `<div style="background:#1e40af;color:#fff;border-radius:50%;width:28px;height:28px;
          display:flex;align-items:center;justify-content:center;font-size:14px;
          border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.4)">🛑</div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      });

      // Carga válvulas desde tu backend (formato GeoJSON)
      const res = await fetch('/api/valvulas');
      const geojson = await res.json();

      geojson.features.forEach((f) => {
        const [lng, lat] = f.geometry.coordinates;
        const p = f.properties || {};
        L.marker([lat, lng], { icon: valveIcon })
          .addTo(map)
          .bindPopup(
            `<b>${p.nombre ?? 'Válvula'}</b><br/>DN ${p.diametro ?? '—'} · ${p.estado ?? '—'}<br/>` +
            `<button data-lat="${lat}" data-lng="${lng}" class="btn-ruta"
              style="margin-top:6px;padding:6px 10px;background:#1e40af;color:#fff;
              border:none;border-radius:6px;cursor:pointer">Trazar ruta</button>`
          );
      });

      // Geolocaliza al operario
      map.locate({ setView: false, enableHighAccuracy: true });
      map.on('locationfound', (e) => {
        posOperario = e.latlng;
        if (userMarker) userMarker.remove();
        userMarker = L.circleMarker(e.latlng, {
          radius: 8, color: '#16a34a', fillColor: '#22c55e', fillOpacity: 1,
        }).addTo(map).bindPopup('Tu posición');
      });
      map.on('locationerror', () => {
        console.warn('Sin acceso a GPS; el operario tendrá que activar ubicación');
      });

      // Traza la ruta al pulsar el botón del popup
      map.on('popupopen', (ev) => {
        const btn = ev.popup._contentNode.querySelector('.btn-ruta');
        if (!btn) return;
        btn.onclick = () => {
          if (!posOperario) {
            alert('Aún no tengo tu ubicación GPS. Activa la localización.');
            return;
          }
          const destino = L.latLng(
            parseFloat(btn.dataset.lat),
            parseFloat(btn.dataset.lng)
          );
          if (routingControl) map.removeControl(routingControl);
          routingControl = L.Routing.control({
            waypoints: [posOperario, destino],
            router: L.Routing.osrmv1({
              serviceUrl: 'https://router.project-osrm.org/route/v1', // ⚠️ solo pruebas
            }),
            lineOptions: { styles: [{ color: '#1e40af', weight: 5 }] },
            createMarker: () => null,
            addWaypoints: false,
            draggableWaypoints: false,
            fitSelectedRoutes: true,
            show: true,
          }).addTo(map);
        };
      });
    })();

    return () => {
      if (mapRef.current) mapRef.current.remove();
    };
  }, []);

  return <div ref={containerRef} style={{ height: '100vh', width: '100%' }} />;
}
