#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Find the dotsy executable in the Python scripts directory
const dotsyPath = path.join(__dirname, '..', '.python-env', 'Scripts', 'dotsy.exe');
const dotsyUnixPath = path.join(__dirname, '..', '.python-env', 'bin', 'dotsy');

function runDotsy(args) {
  // Try Windows path first, then Unix
  const dotsyExecutable = process.platform === 'win32' ? dotsyPath : dotsyUnixPath;
  
  const child = spawn(dotsyExecutable, args, {
    stdio: 'inherit',
    shell: true
  });

  child.on('error', (err) => {
    console.error('Failed to start dotsy:', err.message);
    console.error('\nMake sure dotsy is installed correctly:');
    console.error('  npm install -g dotsy');
    process.exit(1);
  });

  child.on('close', (code) => {
    process.exit(code);
  });
}

// Pass all command line arguments to dotsy
runDotsy(process.argv.slice(2));
