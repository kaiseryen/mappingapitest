fetch("markers.json")
  .then(res => res.json())
  .then(data => {

    data.forEach(m => {
      new mapboxgl.Marker()
        .setLngLat([m.lon, m.lat])
        .setPopup(new mapboxgl.Popup().setText(m.label))
        .addTo(map);
    });

  });