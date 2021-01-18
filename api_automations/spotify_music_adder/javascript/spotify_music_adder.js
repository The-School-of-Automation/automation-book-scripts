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
const scopes = ['user-library-read', 'user-library-modify'];

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

async function setCode(code) {
  const data = await api.authorizationCodeGrant(code);
  api.setAccessToken(data.body['access_token']);
  api.setRefreshToken(data.body['refresh_token']);
}

async function readSavedTracks() {
  const data = await api.getMySavedTracks();
  return data.body.items.map(({ track }) => ({
    id: track.id,
    artist: track.artists[0].name,
    name: track.name,
  }));
}

async function searchTracks(searchTerm) {
  const data = await api.searchTracks(searchTerm);
  return data.body.tracks.items.map(track => ({
    id: track.id,
    artist: track.artists[0].name,
    name: track.name,
  }));
}

async function addTrackFavorites(id) {
  await api.addToMySavedTracks([id]);
}

function printOptions() {
  console.log('0. List saved Tracks');
  console.log('1. Add to Saved Tracks');
  console.log('2. Exit');
}

async function main() {
  // loop
  while (true) {
    printOptions();
    const choice = prompt('What do yo want to do (choose number)? ');
    if (choice == '0') {
      const tracks = await readSavedTracks();
      tracks.forEach(track => console.log(`${track.artist} - ${track.name}`));
      continue;
    }

    if (choice == '1') {
      const searchTerm = prompt('What track do you want to add? ');
      const tracks = await searchTracks(searchTerm);
      tracks.forEach((track, i) => console.log(`${i}. ${track.artist} - ${track.name}`));
      const trackChoice = prompt('Give the number of the right track: ');
      await addTrackFavorites(tracks[Number(trackChoice)].id);
      continue;
    }

    if (choice == '2') break;

    console.log('Try again.');
  }
}

app.get('/', (req, res) => {
  const { code } = req.query;
  res.send('you can close this tab now!');
  server.close();
  setCode(code);
});

//start();

module.exports = {
  searchTracks,
  addTrackFavorites,
  start,
};