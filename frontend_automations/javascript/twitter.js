// npm install dotenv playwright
require('dotenv').config()
const playwright = require('playwright');

// create a .env file
// TWITTER_USERNAME=
// TWITTER_PASSWORD=
const browserType = 'chromium'; // chrome
const username = process.env.TWITTER_USERNAME;
const password = process.env.TWITTER_PASSWORD;

async function main() {
  const browser = await playwright[browserType].launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://twitter.com/login');
  await page.waitForTimeout(1000);

  const inputUsername = await page.$('[name="session[username_or_email]"]');
  await inputUsername.type(username);

  const inputPassword = await page.$('[name="session[password]"]');
  await inputPassword.type(password);

  await inputPassword.press("Enter");

  await page.waitForTimeout(4000);
  const follow = await page.$('[aria-label="Who to follow"]');
  const element = await follow.$('"Show more"');
  await element.click();

  await page.waitForTimeout(4000);
  // use xpath instead of css selector
  const followButtons = await page.$$("//div[contains(@data-testid, '-follow')]");

  let followed = 0;
  const maxFollow = 2;

  for (const button of followButtons) {
    if (followed >= maxFollow) break;

    await button.hover();

    if (Math.random() < .3) {
      // follow this person
      await button.click();
      followed++;
    }

    await page.waitForTimeout(2000);
  }

  console.log('Finished script.');
  await browser.close();
}

main();
