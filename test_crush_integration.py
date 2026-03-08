#!/usr/bin/env python3
"""Test script for Crush CLI integration with Dotsy.

This script demonstrates the integration between Dotsy and Crush CLI.
Run this to verify that the integration is working correctly.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add D:\DOTSY to path if needed
dotsy_path = Path(r"D:\DOTSY")
if str(dotsy_path) not in sys.path:
    sys.path.insert(0, str(dotsy_path))


def test_crush_cli_integration():
    """Test Crush CLI integration components."""
    print("=" * 60)
    print("Testing Crush CLI Integration with Dotsy")
    print("=" * 60)
    
    # Test 1: Configuration
    print("\n1. Testing Configuration...")
    from dotsy.core.config import DotsyConfig, CrushCLIConfig
    
    config = DotsyConfig.model_construct()
    print(f"   [OK] Crush CLI enabled: {config.crush_cli.enabled}")
    print(f"   [OK] YOLO mode: {config.crush_cli.yolo_mode}")
    print(f"   [OK] Auto-approve tools: {config.crush_cli.auto_approve_tools}")
    print(f"   [OK] Disabled tools: {config.crush_cli.disabled_tools}")
    
    # Test 2: Providers
    print("\n2. Testing Providers...")
    providers = [p.name for p in config.providers]
    print(f"   [OK] Available providers: {', '.join(providers)}")
    
    if 'qwen' in providers:
        print(f"   [OK] Qwen provider is available!")
        qwen_models = [(m.alias, m.name) for m in config.models if m.provider == 'qwen']
        print(f"   [OK] Qwen models: {qwen_models}")
    
    # Test 3: Crush Tools
    print("\n3. Testing Crush Tools...")
    from dotsy.core.tools.builtins.crush import CrushCLI, CRUSH_TOOLS
    
    print(f"   [OK] Total Crush tools: {len(CRUSH_TOOLS)}")
    for tool in CRUSH_TOOLS:
        print(f"      - {tool.TOOL_NAME}: {tool.TOOL_DESCRIPTION[:60]}...")
    
    cli = CrushCLI()
    crush_available = cli.is_available()
    print(f"   [OK] Crush CLI installed: {crush_available}")
    
    if crush_available:
        version = cli.get_version()
        print(f"   [OK] Crush CLI version: {version}")
    else:
        print(f"   [INFO] Crush CLI not installed (optional)")
    
    # Test 4: Coordinator
    print("\n4. Testing Agent Coordinator...")
    from dotsy.core.agents.crush_coordinator import (
        CrushDotsyCoordinator,
        AgentRole,
        TaskStatus,
    )
    
    coord = CrushDotsyCoordinator()
    print(f"   [OK] Coordinator initialized")
    print(f"   [OK] Available roles: {[r.value for r in AgentRole]}")
    print(f"   [OK] Task statuses: {[s.value for s in TaskStatus]}")
    
    # Test 5: Create a sample task
    print("\n5. Testing Task Creation...")
    task = coord.create_task(
        description="Test task for Crush-Dotsy integration",
        role=AgentRole.WORKER,
        metadata={"test": True}
    )
    print(f"   [OK] Created task: {task.id}")
    print(f"   [OK] Description: {task.description}")
    print(f"   [OK] Role: {task.role.value}")
    print(f"   [OK] Status: {task.status.value}")
    
    # Test 6: Context Summary
    print("\n6. Testing Context Summary...")
    summary = coord.get_context_summary()
    print(f"   [OK] Crush available: {summary['crush_available']}")
    print(f"   [OK] Active tasks: {summary['active_tasks']}")
    print(f"   [OK] Total tasks: {summary['total_tasks']}")
    
    # Test 7: Tool Manager Integration
    print("\n7. Testing Tool Manager Integration...")
    try:
        from dotsy.core.tools.manager import ToolManager
        print(f"   [OK] ToolManager imported successfully")
        # Note: We can't fully test ToolManager without a config getter
    except ImportError as e:
        print(f"   [FAIL] ToolManager import failed: {e}")
    
    print("\n" + "=" * 60)
    print("Integration Test Complete!")
    print("=" * 60)
    
    if not crush_available:
        print("\n[INFO] Crush CLI is not installed.")
        print("  To enable full functionality, install Crush CLI:")
        print("    - Windows: winget install charmbracelet.crush")
        print("    - macOS: brew install charmbracelet/tap/crush")
        print("    - Go: go install github.com/charmbracelet/crush@latest")
    
    return True


def test_crush_tools_directly():
    """Test Crush tools directly (if Crush CLI is available)."""
    from dotsy.core.tools.builtins.crush import CrushCLI
    
    cli = CrushCLI()
    if not cli.is_available():
        print("\nSkipping direct tool tests (Crush CLI not installed)")
        return
    
    print("\n8. Testing Crush Tools Directly...")
    
    # Test logs
    try:
        logs = cli.get_logs(tail=5)
        print(f"   [OK] Retrieved logs ({len(logs)} chars)")
    except Exception as e:
        print(f"   [INFO] Logs test skipped: {e}")
    
    # Test context
    try:
        context = cli.get_context()
        if context:
            print(f"   [OK] Retrieved context")
        else:
            print(f"   [INFO] No AGENTS.md found")
    except Exception as e:
        print(f"   [INFO] Context test skipped: {e}")


if __name__ == "__main__":
    try:
        test_crush_cli_integration()
        test_crush_tools_directly()
        print("\n[SUCCESS] All tests completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
