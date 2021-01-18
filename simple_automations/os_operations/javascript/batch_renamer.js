const fs = require('fs');
const path = require('path');

const type_filter = '.txt';
const search = 'file';
const replace = 'document';

// filter the current directory for files
const dir = fs.readdirSync('.');
const files = dir.filter(f => fs.statSync(f).isFile());

console.log(`${files.length} of ${dir.length} elements are files.`);

let renamed = 0;

for (const doc of files) {
  const file = path.parse(doc);

  // skip not matching file types
  if (file.ext != type_filter) continue;
  // skip not matching file names
  if (!file.name.includes(search)) continue;

  // rename the actual file
  fs.renameSync(doc, doc.replace(search, replace));
  renamed++;
}

console.log(`renamed ${renamed} of ${files.length} files.`);