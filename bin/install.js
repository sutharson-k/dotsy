#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const PYTHON_ENV_DIR = path.join(__dirname, '..', '.python-env');
const DOTSY_VERSION = require('../package.json').version;

console.log('🐍 Installing DOTSY...');

// Check if Python is installed
function checkPython() {
  try {
    execSync('python --version', { stdio: 'ignore' });
    return 'python';
  } catch {
    try {
      execSync('python3 --version', { stdio: 'ignore' });
      return 'python3';
    } catch {
      console.error('❌ Python 3.12+ is required but not installed.');
      console.error('Please install Python from https://www.python.org/downloads/');
      process.exit(1);
    }
  }
}

// Check if uv is installed, install if not
function checkUv() {
  try {
    execSync('uv --version', { stdio: 'ignore' });
    return true;
  } catch {
    console.log('📦 Installing uv (Python package manager)...');
    try {
      if (process.platform === 'win32') {
        execSync('powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"', { 
          stdio: 'inherit' 
        });
      } else {
        execSync('curl -LsSf https://astral.sh/uv/install.sh | sh', { 
          stdio: 'inherit' 
        });
      }
      return true;
    } catch (err) {
      console.error('❌ Failed to install uv. Please install manually:');
      console.error('  curl -LsSf https://astral.sh/uv/install.sh | sh');
      process.exit(1);
    }
  }
}

// Create Python virtual environment
function createVenv(pythonCmd) {
  console.log('📦 Creating Python environment...');
  
  if (!fs.existsSync(PYTHON_ENV_DIR)) {
    fs.mkdirSync(PYTHON_ENV_DIR, { recursive: true });
  }
  
  try {
    execSync(`uv venv --python 3.12 "${PYTHON_ENV_DIR}"`, { 
      stdio: 'inherit',
      env: { ...process.env, UV_PYTHON_INSTALL_DIR: PYTHON_ENV_DIR }
    });
  } catch (err) {
    console.error('❌ Failed to create virtual environment');
    process.exit(1);
  }
}

// Install dotsy package
function installDotsy() {
  console.log('📦 Installing dotsy package...');
  
  const venvBin = process.platform === 'win32' 
    ? path.join(PYTHON_ENV_DIR, 'Scripts')
    : path.join(PYTHON_ENV_DIR, 'bin');
  
  const pipCmd = process.platform === 'win32'
    ? path.join(venvBin, 'pip.exe')
    : path.join(venvBin, 'pip');
  
  try {
    // Install from PyPI (you need to publish dotsy to PyPI first)
    // OR install from local directory
    execSync(`"${pipCmd}" install -e "${path.join(__dirname, '..')}"`, {
      stdio: 'inherit'
    });
    
    console.log('✅ DOTSY installed successfully!');
    console.log('\n🎉 You can now use dotsy:');
    console.log('   dotsy');
    console.log('\n📚 Documentation: https://github.com/sutharson-k/dotsy');
  } catch (err) {
    console.error('❌ Failed to install dotsy package');
    console.error('Make sure you have published dotsy to PyPI or install locally first');
    process.exit(1);
  }
}

// Main installation flow
function main() {
  const pythonCmd = checkPython();
  checkUv();
  createVenv(pythonCmd);
  installDotsy();
}

main();
