#!/usr/bin/env python3
"""
Quick Cleanup Script
Skip problematic directories, quickly clean up project
"""

import os
import shutil
from pathlib import Path


def quick_cleanup():
    """Quick cleanup, skip problematic directories"""
    print("🚀 Starting quick project cleanup...\n")
    
    # 1. Clean up temporary files
    print("🧹 Cleaning up temporary files...")
    temp_files = [
        "test.py", "test2.py", "test3.py",
        "fadein_20240916091242.mp4", "temp_20240916091242.mp4",
        "test_output.mp4", "test_output1.mp4", "output.mp4",
        ".DS_Store"
    ]
    
    for file_path in temp_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"❌ Skipped: {file_path} ({e})")
    
    # 2. Clean up IDE files
    print("\n🧹 Cleaning up IDE files...")
    ide_dirs = [".idea", "sau/.idea"]
    for dir_path in ide_dirs:
        if Path(dir_path).exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Deleted: {dir_path}")
            except Exception as e:
                print(f"❌ Skipped: {dir_path} ({e})")
    
    # 3. Clean up Python cache
    print("\n🧹 Cleaning up Python cache...")
    cache_dirs = ["__pycache__", "sau/.venv"]
    for dir_path in cache_dirs:
        if Path(dir_path).exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Deleted: {dir_path}")
            except Exception as e:
                print(f"❌ Skipped: {dir_path} ({e})")
    
    # 4. Clean up log files
    print("\n🧹 Cleaning up log files...")
    log_files = ["video_processing.log", "cutvideo/video_processing.log"]
    for file_path in log_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"❌ Skipped: {file_path} ({e})")
    
    # 5. Clean up record files
    print("\n🧹 Cleaning up record files...")
    record_files = [
        "processed_files.txt", "cutvideo/processed_files.txt", 
        "cutvideo/progress.txt", "bilibili_upload_record.txt", 
        "upload_record.json"
    ]
    for file_path in record_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"✅ Deleted: {file_path}")
            except Exception as e:
                print(f"❌ Skipped: {file_path} ({e})")
    
    # 6. Backup conf.py
    print("\n💾 Backing up configuration file...")
    if Path("conf.py").exists():
        backup_dir = Path("backup")
        backup_dir.mkdir(exist_ok=True)
        try:
            shutil.copy2("conf.py", backup_dir / "conf.py")
            print("✅ Backed up conf.py")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
    
    # 7. Skip problematic directories
    print("\n⏭️  Skipping problematic directories...")
    skip_dirs = ["LOCAL_APPDATA_FONTCONFIG_CACHE"]
    for dir_path in skip_dirs:
        if Path(dir_path).exists():
            print(f"⚠️  Skipped: {dir_path} (may be occupied by system)")
    
    print("\n🎉 Quick cleanup completed!")
    print("📋 Suggest manually deleting the following directories (if not needed):")
    print("   - LOCAL_APPDATA_FONTCONFIG_CACHE/")
    print("   - Other problematic directories")


if __name__ == "__main__":
    quick_cleanup() 