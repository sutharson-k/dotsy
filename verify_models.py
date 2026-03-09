import sys
sys.path.insert(0, r'D:\DOTSY')
from dotsy.core.config import DEFAULT_MODELS

print("Last 5 models:")
for m in DEFAULT_MODELS[-5:]:
    print(f"  - {m.alias}: {m.provider}/{m.name}")
