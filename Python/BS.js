'use strict';

const button = document.getElementById('#Named');

function getData(){
 const getIt = fetch('/Flight_game_js/web_start.py')
  .then(response => response.json())
  .then(data => {
    document.querySelector('body').innerHTML = data;
  });

button.onclick = getData;

