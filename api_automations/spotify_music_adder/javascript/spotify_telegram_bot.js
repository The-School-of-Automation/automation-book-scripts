const TelegramBot = require('node-telegram-bot-api');
const { searchTracks, addTrackFavorites, start } = require('./spotify_music_adder');

const TOKEN = 'ENTER BOT TOKEN HERE';
const USERID = 'ENTER YOUR USERID HERE AS INTEGER';

function checkUser(bot, msg) {
  const { id } = msg.chat;
  if (id != USERID) {
    bot.sendMessage(id, 'You are not allowed to use this Bot!');
    return false;
  }
  
  return true;
}

async function setupTelegram(token) {
  // use polling unless you have a public server
  const options = { polling: true };

  const bot = new TelegramBot(token, options);
  // use webhook when polling = false
  // bot.setWebHook(url);

  bot.on('message', async msg => {
    if (!checkUser(bot, msg)) return;
    const { id } = msg.chat;
    const { text } = msg;

    if (text.startsWith('/start')) return;
    
    const tracks = await searchTracks(text);
    const inline_keyboard = [];
    let currentRow = [];
    
    for (const index in tracks) {
      const track = tracks[index];
      const { id, name, artist } = track;
      
      currentRow.push({
        text: `${artist} - ${name}`,
        callback_data: JSON.stringify({ id, name }),
      });
      
      // every second element create a new row
      if (index % 2 == 1) {
        inline_keyboard.push(currentRow);
        currentRow = [];
      }
    }

    const options = { reply_markup: { inline_keyboard } };
    
    bot.sendMessage(id, 'Select the Song to add.', options);
  });
  
  bot.onText(/\/start/, msg => {
    if (!checkUser(bot, msg)) return;
    console.log('test')
    const { id } = msg.chat;
    bot.sendMessage(id, 'Hello, I am the Spotify Music Adder Bot!');
    bot.sendMessage(id, 'Send me a name to search for Spotify Songs and i will present you a list with Songs to add.');
  });
  
  bot.on('callback_query', async callbackQuery => {
      const {
          data,
          message: {
              message_id,
              chat: { id },
          },
      } = callbackQuery;
      const { id: song_id, name } = JSON.parse(data);

      const opts = {
          message_id,
          chat_id: id,
      };

      await addTrackFavorites(song_id);
      // remove markup
      bot.editMessageReplyMarkup(null, opts);
      bot.editMessageText(`Song added: ${name}`, opts);
  });

  return bot;
}

start();
setupTelegram(TOKEN);