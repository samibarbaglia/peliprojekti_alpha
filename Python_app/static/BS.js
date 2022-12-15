'use strict';
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

// global variables

// icons

// form for player name

// function to fetch data from API
async function getData(url){
  const response = await fetch(url);
  if (!response.ok){
    throw new Error('Invalid server input!')
  }
  return response.json();
}

// function to update game status



// function to show weather at selected airport

// function to check if any goals have been reached

// function to update goal data and goal table in UI

// function to check if game is over

// function to set up game
// this is the main function that creates the game and calls the other functions
async function gameSetup() {
  try {
    const response = await getData('http://127.0.0.1:5000/data');
     const data = await response;
    const Arr = Array.from(data);
    for(let location of Arr){
        const name = Object.keys(location);
        const coords = Object.values(location);
        const lat = parseFloat(coords[0]);
        const long = parseFloat(coords[1]);

        const marker = L.marker(lat,long).addTo(map);
        marker.bindPopup(`You are here: <b>${name}</b>`)
    }
  }
  catch(error){
    console.log(error);
  }
}
gameSetup();
// event listener to hide goal splash
