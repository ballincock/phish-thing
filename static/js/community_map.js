let map = null;
let activePinsCache = [];
let leafletMarkersGroup = null;
let currentExpandedPinId = null;

const currentClientUserId = parseInt("{{ user.id }}", 10);

function initLeafletCanvas() {
    map = L.map('mapViewport', { attributionControl: false }).setView([42.08, -87.73], 10);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);

    leafletMarkersGroup = L.layerGroup().addTo(map);

    map.on('click', function(e) {
        openLogModal(e.latlng.lat, e.latlng.lng);
    });
}

async function pullMapPinsPayload() {
    const res = await fetch('/api/community/pins');
    const data = await res.json();
    activePinsCache = data.pins || [];
    
    syncPinsToCanvas();
    renderSidebarPinsList();
}

function syncPinsToCanvas() {
    leafletMarkersGroup.clearLayers();
    
    activePinsCache.forEach(p => {
        const marker = L.circleMarker([p.lat, p.lng], {
            radius: 8,
            fillColor: '#E5509B',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        });

        marker.on('click', (e) => {
            L.DomEvent.stopPropagation(e);
            focusPinNode(p.id, true);
        });

        marker.addTo(leafletMarkersGroup);
        p._markerRef = marker;
    });
}

function renderSidebarPinsList() {
    const q = document.getElementById('pinSearchField').value.toLowerCase();
    const deck = document.getElementById('pinsListDeck');
    deck.innerHTML = '';

    const filtered = activePinsCache.filter(p => 
        p.name.toLowerCase().includes(q) || 
        p.species.toLowerCase().includes(q) || 
        p.creator_name.toLowerCase().includes(q) ||
        p.lure.toLowerCase().includes(q)
    );

    if(filtered.length === 0) {
        deck.innerHTML = '<div style="color:#555; padding:20px; text-align:center; font-size:0.85rem;">No shared coordinates matched query criteria.</div>';
        return;
    }

    filtered.forEach(p => {
        const isExpanded = p.id === currentExpandedPinId;
        const card = document.createElement('div');
        card.id = `sidebar-card-${p.id}`;
        card.style = `padding:15px; border-bottom:1px solid #1e1e1e; cursor:pointer; background:${isExpanded ? '#1e1e1e' : 'transparent'}; transition: background 0.2s;`;
        card.onclick = () => focusPinNode(p.id, false);
        
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:${isExpanded ? 'var(--primary)' : '#fff'}; font-size:0.95rem;">📍 ${p.name}</strong>
                <span style="color:#666; font-size:0.7rem; font-family:monospace;">By: ${p.creator_name}</span>
            </div>
            
            ${isExpanded ? `
                <div style="margin-top:12px; display:flex; flex-direction:column; gap:6px; font-size:0.8rem; color:#ccc; border-top:1px solid #2d2d2d; padding-top:10px;">
                    <div>🐟 <span style="color:#888;">Target Species:</span> <strong>${p.species}</strong></div>
                    <div>🪱 <span style="color:#888;">Lure Profile:</span> <strong>${p.lure}</strong></div>
                    <div>📅 Seasonality: <strong>${p.season}</strong></div>
                    <div style="background:#121212; padding:8px; border-radius:6px; margin-top:4px; display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.75rem;">
                        <div>⏱️ Baro: <span style="color:#fff;">${p.conditions.pressure}</span></div>
                        <div>☁️ Cloud: <span style="color:#fff;">${p.conditions.cloud}</span></div>
                        <div>🌧️ Rain: <span style="color:#fff;">${p.conditions.rain}</span></div>
                        <div>🌡️ Temp: <span style="color:#fff;">${p.conditions.temp}</span></div>
                        <div style="grid-column: 1 / span 2;">💨 Wind: <span style="color:#fff;">${p.conditions.wind}</span></div>
                    </div>
                    
                    
                    ${currentClientUserId === 1 ? `
                        <button onclick="dispatchPinDeletion(${p.id}, event)" style="margin-top:10px; width:100%; border:1px solid #f43f5e; background:none; color:#f43f5e; padding:6px; border-radius:4px; font-size:0.75rem; font-weight:bold; cursor:pointer;">Remove Spot Coordinates (Admin Override)</button>
                    ` : ''}
                </div>
            ` : ''}
        `;
        deck.appendChild(card);
    });
}

function focusPinNode(id, scrollSidebar) {
    currentExpandedPinId = id;
    const pin = activePinsCache.find(p => p.id === id);
    if(!pin) return;

    map.panTo([pin.lat, pin.lng]);
    renderSidebarPinsList();

    if(scrollSidebar) {
        setTimeout(() => {
            const el = document.getElementById(`sidebar-card-${id}`);
            if(el) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 500);
    }
}

function openLogModal(lat, lng) {
    document.getElementById('modalLatField').value = lat;
    document.getElementById('modalLngField').value = lng;
    document.getElementById('modalCoordPreview').value = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
    
    document.getElementById('modalNameField').value = '';
    document.getElementById('modalSpeciesField').value = '';
    document.getElementById('modalLureField').value = '';
    document.getElementById('modalSeasonField').value = '';
    document.getElementById('modalBaroField').value = '';
    document.getElementById('modalCloudField').value = '';
    document.getElementById('modalRainField').value = '';
    document.getElementById('modalTempField').value = '';
    document.getElementById('modalWindField').value = '';

    document.getElementById('pinLogModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('pinLogModal').style.display = 'none';
}

async function dispatchPinCreation(e) {
    e.preventDefault();
    const payload = {
        latitude: document.getElementById('modalLatField').value,
        longitude: document.getElementById('modalLngField').value,
        spot_name: document.getElementById('modalNameField').value.trim(),
        species: document.getElementById('modalSpeciesField').value.trim(),
        lure_used: document.getElementById('modalLureField').value.trim(),
        time_of_year: document.getElementById('modalSeasonField').value.trim(),
        pressure: document.getElementById('modalBaroField').value.trim(),
        cloud_cover: document.getElementById('modalCloudField').value.trim(),
        rain: document.getElementById('modalRainField').value.trim(),
        temp: document.getElementById('modalTempField').value.trim(),
        wind: document.getElementById('modalWindField').value.trim()
    };

    const res = await fetch('/api/community/pins/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if(res.ok) {
        closeModal();
        await pullMapPinsPayload();
        const freshData = await res.json();
        focusPinNode(freshData.pin_id, true);
    } else {
        alert("Failed to publish coordinate parameters onto the global map canvas.");
    }
}

async function dispatchPinDeletion(id, event) {
    event.stopPropagation();
    if(!confirm("ADMIN SECURITY OVERRIDE: Remove this public spot permanently across all community view boards?")) return;

    const res = await fetch(`/api/community/pins/delete/${id}`, { method: 'DELETE' });
    if(res.ok) {
        currentExpandedPinId = null;
        await pullMapPinsPayload();
    } else {
        const errorMsg = await res.json();
        alert(errorMsg.error || "Administrative rejection encountered.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initLeafletCanvas();
    pullMapPinsPayload();
});
