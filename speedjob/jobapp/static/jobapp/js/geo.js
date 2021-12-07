mapboxgl.accessToken = 'pk.eyJ1IjoibnljeiIsImEiOiJja3dvMnloNXAycHN6MnZudmRqNDJ6OXBuIn0.CSWi9vaaVhu62Y4XTaObyg';
const mapboxClient = mapboxSdk({
  accessToken: mapboxgl.accessToken
});
mapboxClient.geocoding
  .forwardGeocode({
    query: '{{company.company_address_city}}, {{company.company_address_plz}}, {{company.company_address_street}}, Germany',
    autocomplete: false,
    limit: 1
  })
  .send()
  .then((response) => {
    if (
      !response ||
      !response.body ||
      !response.body.features ||
      !response.body.features.length
    ) {
      console.error('Invalid response:');
      console.error(response);
      return;
    }
    const feature = response.body.features[0];

    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/dark-v10',
      center: feature.center,
      zoom: 15
    });

    // Create a marker and add it to the map.
    new mapboxgl.Marker().setLngLat(feature.center).addTo(map);
  });
