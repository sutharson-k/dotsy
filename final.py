import subprocess
import os
os.chdir(r'D:\DOTSY')
subprocess.run(['git', 'add', '-A'])
result = subprocess.run(['git', 'commit', '-m', 'chore: Remove temp script'], capture_output=True, text=True)
print(result.stdout)
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
subprocess.run(['git', 'log', '--oneline', '-3'])
