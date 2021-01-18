// npm install argparse
const path = require('path');
const fs = require('fs');
const { ArgumentParser } = require('argparse');

const parser = new ArgumentParser({ description: 'Clean up directory and put files into according folders.' });
parser.addArgument('--path', {
  type: 'string',
  defaultValue: '.',
  help: 'Directory path of the to be cleaned directory',
});

const args = parser.parseArgs();
// rename path variable to dirPath here
const { path: dirPath } = args;

const dir = fs.readdirSync(dirPath);
const files = dir.filter(f => fs.statSync(f).isFile());
const folders = dir.filter(f => fs.statSync(f).isDirectory());

let moved = 0;

console.log(`Cleaning up ${files.length} of ${dir.length} elements.`);

const createdFolders = [];
for (const doc of files) {
  const file = path.parse(doc);

  // skip this script
  if (file.name == 'directory_clean') continue;

  // get name of subfolder to create
  const subfolderPath = path.join(dirPath, file.ext.substring(1));
  
  // create folder if it does not exist
  if (
    !folders.find(f => f == subfolderPath) &&
    !createdFolders.find(f => f == subfolderPath) &&
    !fs.existsSync(subfolderPath)
  ) {
    fs.mkdirSync(subfolderPath);
    createdFolders.push(subfolderPath);
    console.log(`Folder: ${subfolderPath} created.`);
  }

  // move the file to the correct folder
  fs.renameSync(doc, path.join(subfolderPath, file.base));
  moved++;
}

console.log(`Moved ${moved} of ${files.length} files.`);