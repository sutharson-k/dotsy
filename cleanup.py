import subprocess
import os

os.chdir(r'D:\DOTSY')

# Add all changes
subprocess.run(['git', 'add', '-A'])

# Commit
result = subprocess.run(
    ['git', 'commit', '-m', 'chore: Clean up temp scripts'],
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

print("\n=== Final Git Log ===")
subprocess.run(['git', 'log', '--oneline', '-5'])
