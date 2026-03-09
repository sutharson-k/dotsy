import subprocess
import os
os.chdir(r'D:\DOTSY')
subprocess.run(['git', 'add', '-A'])
result = subprocess.run(['git', 'commit', '-m', 'docs: Update README and CHANGELOG with new features'], capture_output=True, text=True)
print(result.stdout)
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
print("\n=== Git Log ===")
subprocess.run(['git', 'log', '--oneline', '-5'])
