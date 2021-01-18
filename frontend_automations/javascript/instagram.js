// create .env file
// USERNAME=
// PASSWORD=

// npm install dotenv playwright
require('dotenv').config()
const playwright = require('playwright');

const browserType = 'chromium'; // chrome
const username = process.env.USERNAME;
const password = process.env.PASSWORD;

async function main() {
  const browser = await playwright[browserType].launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto('http://instagram.com');
  await page.waitForLoadState('load');

  // wait untill page is loaded because instagram is a single page application
  await page.waitForTimeout(3000);

  const inputUsername = await page.$('[name="username"]');
  await inputUsername.type(username, 2000);

  const inputPassword = await page.$('[name="password"]');
  await inputPassword.type(password, 2000);
  await inputPassword.press('Enter');

  await page.waitForTimeout(5000);

  // closes the modal
  const notNow = await page.$('"Not Now"');
  await notNow.click();

  let current = 0;
  while (true) {
    // only get unliked images
    let elements = await page.$$('[aria-label="Like"]');

    // stop if there are no new items
    if (elements.length - 1 == current) break;

    for (; current < elements.length; current++) {
      const element = elements[current];

      // scrolls into view
      await element.hover();
      await page.waitForTimeout(2000);
      
      // like randomly 30% of images
      if (Math.random() > .3) {
        await element.click();
      }
    }
  }

  console.log('Finished the script.');
  await browser.close();
}

main();
