'use strict'

const map = L.map('map', {tap: false});

L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60.1902, 24.5748], 5);

const marker = L.marker([60.1902, 24.5748]).addTo(map);

const username = localStorage.getItem('username');
if (username) {
  const li = document.querySelector('div.stats li:first-child');
  li.innerHTML = "pilot: " + username;
}

// Declare gameData outside of functions so it is available to both gameSetup() and flyTo()
const gameData = {
  location: [
    {
      name: 'Helsinki Airport',
      latitude: 60.1902,
      longitude: 24.5748,
      active: true
    },
    {
      name: 'Vantaa Airport',
      latitude: 60.2802,
      longitude: 24.9348,
      active: false
    }
  ]
};

async function gameSetup() {
  try {
    for (let airport of gameData.location) {
      const marker = L.marker([airport.latitude, airport.longitude]).addTo(map);
      if (airport.active === true) {
        marker.bindPopup(`Current location: <b>${airport.name}</b>`);
        marker.openPopup();
      }
    }

  } catch (error) {
    console.log(error);
  }
}

async function getData() {
  // Fetches the necessary data from Flask
  const landings = await fetch('http://127.0.0.1:5000/get_coords')
  const planeFetch = await fetch('http://127.0.0.1:5000/get_plane');
  const plane = await planeFetch.json();
  console.log(landings, plane, planeFetch)
}

function intoGameData(data, gameData) {
  gameData = {location: []};
  for (const item in data) {
    const name = item[0];
    const latitude = item[1];
    const longitude = item[2];
    const details = {
      name: name,
      latitude: latitude,
      longitude: longitude,
      active: false
    }
    gameData['location'].push(details);
  }
  return gameData;
}


function addMarkersForCoordinates(coordinates) {
  coordinates.forEach(coordinate => {
    const [latitude, longitude] = coordinate;
    const marker = L.marker([latitude, longitude]).addTo(map);
  });
}

getData();
