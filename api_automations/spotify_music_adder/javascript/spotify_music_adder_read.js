// npm install spotify-web-api-node express cors open prompt-sync
const SpotifyWebApi = require('spotify-web-api-node');
const prompt = require('prompt-sync')();
const express = require('express');
const cors = require('cors');
const open = require('open');

const app = express();
app.use(cors());
let server = null;

const clientId = 'ENTER CLIENT ID HERE';
const clientSecret = 'ENTER CLIENT SECRET HERE';
const scopes = ['user-library-read'];

const api = new SpotifyWebApi({
  clientId,
  clientSecret,
  redirectUri: 'http://localhost:8080',
});

async function start() {
  const url = await api.createAuthorizeURL(scopes, 'randomstate');
  server = app.listen(8080);
  open(url);
}

async function readSavedTracks() {
  const data = await api.getMySavedTracks();
  return data.body.items.map(({ track }) => ({
    id: track.id,
    artist: track.artists[0].name,
    name: track.name,
  }));
}

function printOptions() {
  console.log('0. List saved Tracks');
  console.log('1. Exit');
}

async function main(code) {
  const data = await api.authorizationCodeGrant(code);
  api.setAccessToken(data.body['access_token']);
  api.setRefreshToken(data.body['refresh_token']);
  
  // loop
  while (true) {
    printOptions();
    const choice = prompt('What do yo want to do (choose number)? ');
    if (choice == '0') {
      const tracks = await readSavedTracks();
      tracks.forEach(track => console.log(`${track.artist} - ${track.name}`));
      continue;
    }

    if (choice == '1') break;

    console.log('Try again.');
  }
}

app.get('/', (req, res) => {
  const { code } = req.query;
  res.send('you can close this tab now!');
  server.close();
  main(code);
});

start();