#!/usr/bin/env node

/**
 * DOTSY Update Script
 * 
 * Usage:
 *   node bin/update.js [new_version]
 * 
 * Examples:
 *   node bin/update.js        # Auto-increment patch version
 *   node bin/update.js 1.2.3  # Set specific version
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PACKAGE_JSON_PATH = path.join(__dirname, '..', 'package.json');
const PYPROJECT_TOML_PATH = path.join(__dirname, '..', 'pyproject.toml');

// Parse version string into components
function parseVersion(version) {
  const parts = version.split('.').map(Number);
  return {
    major: parts[0] || 0,
    minor: parts[1] || 0,
    patch: parts[2] || 0
  };
}

// Increment patch version
function incrementVersion(version) {
  const v = parseVersion(version);
  v.patch++;
  return `${v.major}.${v.minor}.${v.patch}`;
}

// Update package.json version
function updatePackageJson(newVersion) {
  const packageJson = JSON.parse(fs.readFileSync(PACKAGE_JSON_PATH, 'utf-8'));
  packageJson.version = newVersion;
  fs.writeFileSync(PACKAGE_JSON_PATH, JSON.stringify(packageJson, null, 2) + '\n');
  console.log(`✅ Updated package.json to v${newVersion}`);
}

// Update pyproject.toml version
function updatePyProjectToml(newVersion) {
  let content = fs.readFileSync(PYPROJECT_TOML_PATH, 'utf-8');
  content = content.replace(
    /version = "[\d.]+"/,
    `version = "${newVersion}"`
  );
  fs.writeFileSync(PYPROJECT_TOML_PATH, content);
  console.log(`✅ Updated pyproject.toml to v${newVersion}`);
}

// Commit and tag
function commitAndTag(newVersion) {
  try {
    execSync(`git add package.json pyproject.toml`, { stdio: 'inherit' });
    execSync(`git commit -m "chore: bump version to v${newVersion}"`, { stdio: 'inherit' });
    execSync(`git tag v${newVersion}`, { stdio: 'inherit' });
    console.log(`✅ Committed and tagged v${newVersion}`);
  } catch (err) {
    console.error('❌ Failed to commit/tag. Make sure git is configured.');
  }
}

// Publish to npm
function publishToNpm() {
  console.log('📦 Publishing to npm...');
  try {
    execSync('npm publish', { stdio: 'inherit' });
    console.log('✅ Published to npm!');
  } catch (err) {
    console.error('❌ Failed to publish to npm');
    console.error('Make sure you are logged in: npm login');
  }
}

// Main
function main() {
  const packageJson = JSON.parse(fs.readFileSync(PACKAGE_JSON_PATH, 'utf-8'));
  const currentVersion = packageJson.version;
  
  let newVersion;
  if (process.argv[2]) {
    newVersion = process.argv[2];
  } else {
    newVersion = incrementVersion(currentVersion);
  }
  
  console.log(`🔄 Updating DOTSY from v${currentVersion} to v${newVersion}\n`);
  
  updatePackageJson(newVersion);
  updatePyProjectToml(newVersion);
  commitAndTag(newVersion);
  
  console.log('\n📦 Ready to publish!');
  console.log('Run: npm publish');
  console.log('Then: git push origin main --tags');
}

main();
