# DOTSY Development & Release Guide

## How to Update DOTSY

### Quick Update (Auto-increment Patch Version)

```bash
# 1. Run update script (auto-increments patch: 1.0.0 → 1.0.1)
node bin/update.js

# 2. Publish to npm
npm publish

# 3. Push to GitHub
git push origin main --tags
```

### Specific Version Update

```bash
# Set specific version
node bin/update.js 1.2.3

# Publish
npm publish

# Push
git push origin main --tags
```

## What the Update Script Does

1. ✅ Updates `package.json` version
2. ✅ Updates `pyproject.toml` version
3. ✅ Commits changes to git
4. ✅ Creates git tag (e.g., `v1.2.3`)
5. ✅ Prepares for npm publish

## Manual Update Steps (Alternative)

If you prefer manual control:

### 1. Update Version Numbers

**package.json:**
```json
{
  "name": "dotsy",
  "version": "1.2.3"  // ← Update this
}
```

**pyproject.toml:**
```toml
[project]
name = "dotsy"
version = "1.2.3"  // ← Update this
```

### 2. Commit and Tag

```bash
git add package.json pyproject.toml
git commit -m "chore: bump version to v1.2.3"
git tag v1.2.3
```

### 3. Publish to npm

```bash
npm publish
```

### 4. Push to GitHub

```bash
git push origin main --tags
```

## Version Numbering (SemVer)

DOTSY uses [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., `1.2.3`)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Examples

```
1.0.0 → 1.0.1  # Bug fix (patch)
1.0.1 → 1.1.0  # New feature (minor)
1.1.0 → 2.0.0  # Breaking change (major)
```

## Testing Before Publishing

### Test Locally

```bash
# Link package locally
npm link

# Test the command
dotsy --version

# Unlink when done
npm unlink
```

### Test Installation

```bash
# Create test directory
mkdir test-dotsy && cd test-dotsy

# Install from local path
npm install -g /path/to/dotsy

# Test
dotsy --version

# Cleanup
npm uninstall -g dotsy
```

## Publishing to PyPI (Optional)

If you also want to publish to PyPI:

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

Users can then install via:
```bash
pip install dotsy
```

## Release Checklist

Before publishing:

- [ ] Update version numbers
- [ ] Run tests: `uv run pytest`
- [ ] Update CHANGELOG.md with changes
- [ ] Update README.md if needed
- [ ] Commit and tag
- [ ] Test locally with `npm link`
- [ ] Publish to npm
- [ ] Push to GitHub with tags
- [ ] (Optional) Publish to PyPI

## Users Updating DOTSY

Users can update with:

```bash
# npm installation
npm update -g dotsy

# Or reinstall
npm install -g dotsy@latest

# pip installation
pip install --upgrade dotsy

# uv installation
uv tool upgrade dotsy
```

## Troubleshooting

### npm publish fails

```bash
# Make sure you're logged in
npm login

# Check if version already exists
npm view dotsy versions

# If version exists, increment and try again
node bin/update.js
npm publish
```

### Git tag already exists

```bash
# Delete old tag locally and remotely
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3

# Create new tag
git tag v1.2.3
git push origin --tags
```

## Support

- GitHub Issues: https://github.com/sutharson-k/dotsy/issues
- Documentation: https://github.com/sutharson-k/dotsy#readme
