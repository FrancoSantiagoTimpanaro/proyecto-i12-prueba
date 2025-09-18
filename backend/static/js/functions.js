// =======================
// Configuración del mapa
// =======================
const MapModule = (() => {
  let map;

  function initMap(center = [-34.92145, -57.95453], zoom = 14) {
    map = L.map('map').setView(center, zoom);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    return map;
  }

  function addMarker(name, lat, lng) {
    if (!map) return;
    L.marker([lat, lng]).addTo(map).bindPopup(`<b>${name}</b>`).openPopup();
  }

  function setView(lat, lng, zoom = 16) {
    if (!map) return;
    map.setView([lat, lng], zoom);
  }

  return { initMap, addMarker, setView };
})();

// =======================
// Carga de ubicaciones
// =======================
const LocationsModule = (() => {
  async function loadLocations() {
    try {
      const res = await fetch("/locations");
      const data = await res.json();
      data.forEach(loc => MapModule.addMarker(loc.name, loc.lat, loc.lng));
    } catch (err) {
      console.error("Error cargando ubicaciones:", err);
    }
  }

  return { loadLocations };
})();

// =======================
// Manejo de formulario
// =======================
const FormModule = (() => {

  async function geocodeIntersection(intersection) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(intersection)}`;
    const res = await fetch(url);
    const data = await res.json();
    if (data.length > 0) {
      return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) };
    } else {
      throw new Error("No se encontró la intersección 😕");
    }
  }

  async function saveLocation(name, intersection, lat, lng) {
    const res = await fetch("/add_location", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, intersection, lat, lng })
    });
    return await res.json();
  }

  function setupForm() {
    const form = document.getElementById("locationForm");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const intersection = document.getElementById("intersection").value;

      try {
        const coords = await geocodeIntersection(intersection);
        MapModule.addMarker(name, coords.lat, coords.lng);
        MapModule.setView(coords.lat, coords.lng);

        const result = await saveLocation(name, intersection, coords.lat, coords.lng);
        console.log("Guardado en DB:", result);

        form.reset();
      } catch (err) {
        alert(err.message);
      }
    });
  }

  return { setupForm };
})();

// =======================
// Inicialización al cargar
// =======================
window.onload = () => {
  MapModule.initMap();
  LocationsModule.loadLocations();
  FormModule.setupForm();
};