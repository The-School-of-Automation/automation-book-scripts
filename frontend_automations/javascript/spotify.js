// npm install puppeteer dotenv playwright
require('dotenv').config()
//const playwright = require('playwright');
const puppeteer = require('puppeteer');

// create a file called .env
// SPOTIFY_USERNAME=
// SPOTIFY_PASSWORD=
const browserType = 'chromium'; // chrome
const username = process.env.SPOTIFY_USERNAME;
const password = process.env.SPOTIFY_PASSWORD;

async function main() {
  //const browser = await playwright[browserType].launch({ headless: false });

  // Article for different platforms
  // https://medium.com/@jaredpotter1/connecting-puppeteer-to-existing-chrome-window-8a10828149e0
  // command to start a chrome instance (from the article)
  // google-chrome-stable --remote-debugging-port=9222 --user-data-dir=remote-profile
  // copy the endpoint here
  const browserWSEndpoint = 'ws://127.0.0.1:9222/devtools/browser/010f749a-f1be-45ac-b606-6e00abc417ee';
  const browser = await puppeteer.connect({ browserWSEndpoint });

  const page = await browser.newPage()
  // compat the existing function so the existing code doesn't have to be changed
  page.waitForTimeout = page.waitFor;

  await page.goto('https://accounts.spotify.com/en/login');

  await page.waitForTimeout(2000);
  const inputUsername = await page.$('[ng-model="form.username"]');
  await inputUsername.type(username);

  const inputPassword = await page.$('[ng-model="form.password"]');
  await inputPassword.type(password);
  await inputPassword.press('Enter');

  await page.waitForTimeout(3000);

  // copy playlist URL here
  const playlistURL = 'https://open.spotify.com/playlist/2YOMHgtmYN1Jt6Jqqowq7Z';
  await page.goto(playlistURL);
  await page.waitForTimeout(5000);

  const playButtons = await page.$$('[title="Play"]');
  const playButton = playButtons[1];

  await playButton.hover();
  await playButton.click();
  console.log('start listening!')
}

main();
