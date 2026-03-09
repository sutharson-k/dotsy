import subprocess
import os

os.chdir(r'D:\DOTSY')

# Add all changes
subprocess.run(['git', 'add', '-A'])

# Commit
result = subprocess.run(
    ['git', 'commit', '-m', 'feat: Add /set-api-key command for chat interface

- Add /set-api-key, /apikey, /api-key aliases
- Parse provider name and API key from command
- Save to ~/.dotsy/.env using dotenv
- Show usage help with available providers
- Display success/error messages in chat'],
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
