'use strict'
const map = L.map('map', {tap: false });

L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60.1902, 24.5748], 5);

let marker = L.marker([60.1902, 24.5748]).addTo(map);

/* TOINEN KARTTA */
/* let map = L.map('map').setView([60.1902, 24.5748], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 4,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let marker = L.marker([60.1902, 24.5748]).addTo(map);
 */
