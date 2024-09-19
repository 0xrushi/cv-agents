const fs = require('fs');
const path = require('path');

function findPdfWorkerFile(startPath) {
  const files = fs.readdirSync(startPath);
  for (const file of files) {
    const filename = path.join(startPath, file);
    const stat = fs.lstatSync(filename);
    if (stat.isDirectory()) {
      const found = findPdfWorkerFile(filename);
      if (found) return found;
    } else if (filename.endsWith('pdf.worker.min.js')) {
      return filename;
    }
  }
  return null;
}

const nodeModulesPath = path.join(__dirname, 'node_modules');
const sourceFile = findPdfWorkerFile(nodeModulesPath);
const destinationFile = path.join(__dirname, 'public', 'pdf.worker.min.js');

if (sourceFile) {
  fs.copyFile(sourceFile, destinationFile, (err) => {
    if (err) {
      console.error('Error copying file:', err);
    } else {
      console.log('pdf.worker.min.js was copied to public/');
    }
  });
} else {
  console.error('Could not find pdf.worker.min.js in node_modules');
}