// npm install argparse
const fs = require('fs');
const path = require('path');
const { ArgumentParser } = require('argparse');

const parser = new ArgumentParser({ description: 'Batch rename files in directory' }); parser.addArgument('search', { type: 'string', help: 'To be replaced text' }); parser.addArgument('replace', { type: 'string', help: 'Text to use for replacement' }); parser.addArgument('--filetype', {
  type: 'string',
  defaultValue: null,
  help: 'Only files with the given type will be renamed (e.g. .txt)',
});
parser.addArgument('--path', {
  type: 'string',
  defaultValue: '.',
  help: 'Directory path that contains the to be renamed files',
});

const args = parser.parseArgs();
console.log(args);

// rename path to dirPath because of naming conflict with the path library
const { filetype, search, replace, path: dirPath } = args;

// filter the current directory for files
const dir = fs.readdirSync(dirPath);
const files = dir.filter(f => fs.statSync(f).isFile());

console.log(`${files.length} of ${dir.length} elements are files.`);

let renamed = 0;

for (const doc of files) {
  const file = path.parse(doc);

  // skip not matching file types
  if (filetype != null && file.ext != filetype) continue;
  // skip not matching file names
  if (!file.name.includes(search)) continue;

  // rename the actual file
  fs.renameSync(doc, doc.replace(search, replace));
  renamed++;
}

console.log(`renamed ${renamed} of ${files.length} files.`);