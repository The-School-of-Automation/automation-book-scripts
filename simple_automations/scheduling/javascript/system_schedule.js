const fs = require('fs');

const dir = fs.readdirSync('.');
const files = dir.filter(f => fs.statSync(f).isFile());
const now = new Date();
const filename = 'summary.log';

fs.appendFileSync(filename, now + '\n');
files.forEach(file => fs.appendFileSync(filename, `\t${file}\n`));
fs.appendFileSync(filename, '\n');

console.log(`Wrote ${files.length} entries for ${now} to summary.log`);