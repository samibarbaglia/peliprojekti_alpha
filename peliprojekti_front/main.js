let map = L.map('map').setView([60.1902, 24.5748], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 4,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let marker = L.marker([60.1902, 24.5748]).addTo(map);

var markerColor = L.marker({
})