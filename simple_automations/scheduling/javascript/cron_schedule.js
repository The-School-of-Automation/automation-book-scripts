// npm install node-schedule
const cron = require('node-schedule');
const os = require('os');
const path =  require('path');
const fs = require('fs');

const oldFilesFolderName = 'old_files';
const downloadsFolder = path.join(os.homedir(), 'Downloads', 'test');
const oldFilesFolderPath = path.join(downloadsFolder, oldFilesFolderName);

function cleanUpDownloads() {
  console.log('Starting Cleanup');
  // create old files folder
  if (!fs.existsSync(oldFilesFolderPath)) {
    fs.mkdirSync(oldFilesFolderPath);
    console.log('Created old files folder');
  }

  const now = new Date();
  // months start at 0 so add 1
  const timestamp = `${now.getFullYear()}_${now.getMonth() + 1}_${now.getDate()}`;
  
  // create new folder with todays timestamp
  const dateFolder = path.join(oldFilesFolderPath, timestamp);
  if (!fs.existsSync(dateFolder)) {
    fs.mkdirSync(dateFolder);
    console.log('Created Date Folder.');
  }
  
  // get all items from downloads folder
  const dir = fs.readdirSync(downloadsFolder);
  
  let moved = 0;
  // move items to new folder
  for (const item of dir.filter(f => !f.includes(oldFilesFolderName))) {
    fs.renameSync(path.join(downloadsFolder, item), path.join(dateFolder, item));
    moved++;
  }

  console.log(`Cleaned ${moved} files.`);
}

// uncomment for testing
//cleanUpDownloads();

// every monday at 12 o clock
cron.scheduleJob('0 12 * * MON', cleanUpDownloads);