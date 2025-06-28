#!/usr/bin/env python3
"""
Final Cleanup Script
Simple and fast cleanup of remaining files
"""

import os
import shutil
from pathlib import Path


def final_cleanup():
    """Final cleanup"""
    print("🧹 Final cleanup...")
    
    # 1. Delete empty cutvideo directory
    if Path("cutvideo").exists():
        try:
            if not any(Path("cutvideo").iterdir()):
                shutil.rmtree("cutvideo")
                print("✅ Deleted empty directory: cutvideo")
        except Exception as e:
            print(f"❌ Failed to delete cutvideo: {e}")
    
    # 2. Delete empty sau directory
    if Path("sau").exists():
        try:
            if not any(Path("sau").iterdir()):
                shutil.rmtree("sau")
                print("✅ Deleted empty directory: sau")
        except Exception as e:
            print(f"❌ Failed to delete sau: {e}")
    
    # 3. Delete virtual environment
    if Path(".venv").exists():
        try:
            shutil.rmtree(".venv")
            print("✅ Deleted virtual environment: .venv")
        except Exception as e:
            print(f"❌ Failed to delete .venv: {e}")
    
    # 4. Delete Python cache
    if Path("__pycache__").exists():
        try:
            shutil.rmtree("__pycache__")
            print("✅ Deleted Python cache: __pycache__")
        except Exception as e:
            print(f"❌ Failed to delete __pycache__: {e}")
    
    # 5. Delete empty data directories
    empty_dirs = []
    for item in Path("data").iterdir():
        if item.is_dir() and not any(item.iterdir()):
            empty_dirs.append(item)
    
    for empty_dir in empty_dirs:
        try:
            empty_dir.rmdir()
            print(f"✅ Deleted empty directory: {empty_dir}")
        except Exception as e:
            print(f"❌ Failed to delete {empty_dir}: {e}")
    
    print("\n🎉 Final cleanup completed!")


if __name__ == "__main__":
    final_cleanup() 