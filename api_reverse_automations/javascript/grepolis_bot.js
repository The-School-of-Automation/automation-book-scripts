// npm install axios
const axios = require('axios').default;

const cookies = {};

const session = axios.create();
session.defaults.withCredentials = true;
session.defaults.headers['user-agent'] = 'Chrome/51.0.2704.63';

function parseCookies(response) {
  const setCookies = response.headers['set-cookie'];

  for (const cookie of setCookies) {
    const pair = cookie.split(';')[0].split('=')
    cookies[pair[0]] = pair[1];
  }

  let cookieString = '';
  for (const key of Object.keys(cookies)) {
    cookieString += `${key}=${cookies[key]}; `;
  }

  session.defaults.headers['Cookie'] = cookieString.trim();
}

const noRedirectOptions = {
  maxRedirects: 0,
  validateStatus: status => status >= 200 && status < 303,
};

async function main() {
  const baseURL = 'https://en.grepolis.com/';
  const initialRequest = await session.get(baseURL);
  parseCookies(initialRequest);

  session.defaults.headers['X-Requested-With'] = 'XMLHttpRequest';
  session.defaults.headers['X-XSRF-TOKEN'] = cookies['XSRF-TOKEN']

  const loginCheckURL = 'https://en.grepolis.com/glps/login_check';

  const username = 'scriptworld';
  const password = 'udemy123';

  const loginCheckPayload = `login%5Buserid%5D=${username}&login%5Bpassword%5D=${password}&login%5Bremember_me%5D=true`

  const loginCheck = await session.post(loginCheckURL, loginCheckPayload);
  parseCookies(loginCheck);

  const re1 = await session.get(baseURL, noRedirectOptions);
  parseCookies(re1);

  const re2 = await session.get(re1.headers.location, noRedirectOptions);
  parseCookies(re2);

  const fre = await session.get('https://en0.grepolis.com/start/index');
  const csrfdata = fre.data;
  const start = csrfdata.indexOf('CSRF.token = ') + 14;
  const end = csrfdata.indexOf("'", start);
  const token = csrfdata.substring(start, end);

  const gameworld = 'en126';
  const gameworldPayload = `world=${gameworld}&facebook_session=&facebook_login=&token=${token}&portal_sid=&name=${username}&password=`;

  const gameworldURL = 'https://en0.grepolis.com/start?action=login_to_game_world';

  const gre1 = await session.post(gameworldURL, gameworldPayload, noRedirectOptions);
  parseCookies(gre1);
  const gre2 = await session.get(gre1.headers.location, noRedirectOptions);
  parseCookies(gre2);

  const baseGameURL = `https://${gameworld}.grepolis.com`;

  const gameRe = await session.get(baseGameURL + gre2.headers.location);
  parseCookies(gameRe);
  const startToken = gameRe.data.indexOf('csrfToken') + 12;
  const endToken = gameRe.data.indexOf('"', startToken);
  const hparameter = gameRe.data.substring(startToken, endToken);
  console.log(Date.now())

  const testRe = `https://${gameworld}.grepolis.com/game/building_barracks?town_id=10947&action=index&h=${hparameter}&json={"town_id":10947,"nl_init":true}&_=${Date.now()}`;

  const lastRe = await session.get(testRe);
  console.log(lastRe.data);
}

main();
