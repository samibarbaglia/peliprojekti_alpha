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



async function gameSetup() {
  try {
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
    }
      for(let airport of gameData.location) {
      const marker = L.marker([airport.latitude, airport.longitude]).addTo(map);
      if(airport.active === true) {
        marker.bindPopup(`Current location: <b>${airport.name}</b>`);
        marker.openPopup();
      }
    }

  } catch (error) {
      console.log(error);
  }
}
async function getData() {
  const plane = await fetch('http://127.0.0.1:5000/get_plane');
  const data = await plane.json();
  const dataReq = await fetch('http://127.0.0.1:5000/game/fly/' + plane, {method: 'GET'})
    .then(response => response.json())
    .then(data => {
      document.querySelector('#testing').innerHTML = 'Plane: ${data{{key}}} <br> json: ${data{{value}}}'
    });
  return data
}

async function flyTo() {
  const data = await getData();

  for (const coordinate of data) {
    const marker = L.marker([coordinate.latitude, coordinate.longitude]).addTo(map);
    marker.bindPopup(`Current location: <b>${coordinate.name}</b>`);
    marker.openPopup();
  }
}

window.onload = function() {
  // call flyTo() function after the page has loaded
  flyTo();
};