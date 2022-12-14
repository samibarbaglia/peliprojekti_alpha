'use strict'
const map = L.map('map', {tap: false });

L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60.1902, 24.5748], 5);

let marker = L.marker([60.1902, 24.5748]).addTo(map);

const username = localStorage.getItem('username');
if (username) {
  const li = document.querySelector('div.stats li:first-child');
  li.innerHTML = username;
}

