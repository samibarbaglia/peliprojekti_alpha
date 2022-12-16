'use strict';
const map = L.map('map', {tap: false});

L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
  map.setView([60.1902, 24.5748], 5);


const username = localStorage.getItem('username');
if (username) {
  const li = document.querySelector('div.stats li:first-child');
  li.innerHTML = "pilot: " + username;
}

/* PLACEHOLDER DESTINATION BOX */
const destination = "tää";
const li = document.querySelector('div.stats li:nth-child(2)');
li.innerHTML = "destination: " + destination;



// function to fetch data from API
async function getData(url){
  const response = await fetch(url);
  if (!response.ok){
    throw new Error('Invalid server input!')
  }
  return response.json();
}

// function to update game status
function updateData(data){
  const url = 'http://127.0.0.1:5000/update'
  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
  gameSetup();
}

// function to check if any goals have been reached

// function to set up game
// this is the main function that creates the game and calls the other functions
async function gameSetup() {
  try {
    //Fetch the map details
    const response = await getData('http://127.0.0.1:5000/data');
    const data = await response;
    //Fetch player's location
    const locRes = await getData('http://127.0.0.1:5000/get_location');
    const currentlyArr = await locRes;
    const currently = Object.keys(currentlyArr)[0]

    const Arr = Array.from(data);
    for (let location of Arr) {
      const name = Object.keys(location)[0];
      const data = Object.values(location);
      const coords = data[0];
      // Create a new marker for the current location
      const marker = L.marker(coords).addTo(map);
      if (name === currently) {
        //Here goes a way to tell current location apart from other markers
      } else {
        const clickContent = document.createElement('div');
        const h4 = document.createElement('h4');
        h4.innerHTML = name;
        clickContent.append(h4);
        const buttonMe = document.createElement('button');
        buttonMe.innerHTML = 'Fly here';
        clickContent.append(buttonMe);

       buttonMe.addEventListener('click', function(e){
              //Updating the location
            const newData = {[name]: coords};
            console.log(newData);
            updateData(newData);
})
        marker.bindPopup(clickContent);
        marker.openPopup();
      }}}
  catch
    (error)
    {
      console.log(error);
    }
  }
gameSetup();
// event listener to hide goal splash
