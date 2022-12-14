'use strict'
const map = L.map('map', {tap: false});

L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60.1902, 24.5748], 5);

const marker = L.marker([60.1902, 24.5748]).addTo(map);
marker.bindPopup(`Current location: <b>${airport.name}</b>`)


async function gameSetup() {
  try {
    const gameData = await getData('testdata/newgame.json');
    console.log(gameData)

    for(let airport of gameData.location) {
      const marker = L.marker([airport.latitude, airport.longitude]).addTo(map);
      if(airport.active === true) {
        marker.bindPopup(`Current location: <b>${airport.name}</b>`);
      }
    }

  } catch (error) {
      console.log(error);
  }
}

gameSetup();