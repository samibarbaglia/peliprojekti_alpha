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

/* PLACEHOLDER DESTINATION BOX */
const destination = "tää";
const li = document.querySelector('div.stats li:nth-child(2)');
li.innerHTML = "destination: " + destination;



async function gameSetup() {
  try {
    const gameData = await getData('testdata/newgame.json');
    console.log(gameData)

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

async function getData(){
  fetch('/data')
      .then((response) => response.json())
  .then((data) => {
    document.querySelector('#testing').innerHTML = data;
  });

}

async function flyTo(){
    let data = await getData()
    document.querySelector('#mapUn').innerHTML = data;
    try {
      for(let airport in locations) {
      const marker = L.marker([airport.location]).addTo(map);
      if(airport.active === true) {
        marker.bindPopup(`Current location: <b>${airport.name}</b>`);
        marker.openPopup();
      }
    }

  } catch (error) {
      console.log(error);
  }
}

gameSetup();
flyTo();