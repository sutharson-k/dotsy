import subprocess
import os

os.chdir(r'D:\DOTSY')

# Add all changes
subprocess.run(['git', 'add', '-A'])

# Commit
result = subprocess.run(
    ['git', 'commit', '-m', 'fix: Show all slash commands in autocomplete

- Increase MAX_SUGGESTIONS_COUNT from 10 to 20
- Clear Python cache for proper command loading'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Push to main
result = subprocess.run(
    ['git', 'push', 'origin', 'main'],
    capture_output=True,
    text=True
)
print(result.stdout)

print("\n=== Git Log ===")
subprocess.run(['git', 'log', '--oneline', '-5'])
