import subprocess
import os

os.chdir(r'D:\DOTSY')

# Add all changes
subprocess.run(['git', 'add', '-A'])

# Commit
result = subprocess.run(
    ['git', 'commit', '-m', 'chore: Clean up temp files'],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Push to main
result = subprocess.run(
    ['git', 'push', 'origin', 'main'],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)

print("\n=== Final Status ===")
subprocess.run(['git', 'log', '--oneline', '-5'])
