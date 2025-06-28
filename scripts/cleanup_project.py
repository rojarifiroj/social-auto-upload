#!/usr/bin/env python3
"""
Project Cleanup Script
Delete unnecessary files and directories
"""

import os
import shutil
import time
from pathlib import Path


def cleanup_temp_files():
    """Clean up temporary files"""
    print("🧹 Cleaning up temporary files...")
    
    temp_files = [
        # Test files
        "test.py",
        "test2.py", 
        "test3.py",
        
        # Temporary video files
        "fadein_20240916091242.mp4",
        "temp_20240916091242.mp4",
        "test_output.mp4",
        "test_output1.mp4",
        "output.mp4",
        
        # System files
        ".DS_Store",
    ]
    
    for file_path in temp_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"✅ Deleted temporary file: {file_path}")
            except Exception as e:
                print(f"❌ Failed to delete {file_path}: {e}")


def cleanup_ide_files():
    """Clean up IDE files"""
    print("🧹 Cleaning up IDE files...")
    
    ide_dirs = [
        ".idea",
        "sau/.idea",
    ]
    
    for dir_path in ide_dirs:
        if Path(dir_path).exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Deleted IDE directory: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to delete {dir_path}: {e}")


def cleanup_cache_files():
    """Clean up cache files"""
    print("🧹 Cleaning up cache files...")
    
    cache_dirs = [
        "__pycache__",
        "sau/.venv",
    ]
    
    for dir_path in cache_dirs:
        if Path(dir_path).exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Deleted cache directory: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to delete {dir_path}: {e}")
    
    # Special handling for font cache directory
    font_cache_dir = "LOCAL_APPDATA_FONTCONFIG_CACHE"
    if Path(font_cache_dir).exists():
        print(f"⚠️  Found font cache directory: {font_cache_dir}")
        response = input("Try to delete font cache directory? (y/N): ")
        if response.lower() == 'y':
            try:
                # First try to delete files
                for file_path in Path(font_cache_dir).glob("*"):
                    try:
                        if file_path.is_file():
                            file_path.unlink()
                            print(f"  ✅ Deleted file: {file_path.name}")
                        elif file_path.is_dir():
                            shutil.rmtree(file_path)
                            print(f"  ✅ Deleted subdirectory: {file_path.name}")
                    except Exception as e:
                        print(f"  ⚠️  Skipped file: {file_path.name} ({e})")
                
                # Then delete main directory
                time.sleep(1)  # Wait a bit
                shutil.rmtree(font_cache_dir)
                print(f"✅ Deleted font cache directory: {font_cache_dir}")
            except Exception as e:
                print(f"❌ Failed to delete font cache directory: {e}")
                print("💡 Suggestion: Can manually delete or delete after restart")
        else:
            print(f"⏭️  Skipped font cache directory: {font_cache_dir}")


def cleanup_log_files():
    """Clean up log files"""
    print("🧹 Cleaning up log files...")
    
    log_files = [
        "video_processing.log",
        "cutvideo/video_processing.log",
    ]
    
    for file_path in log_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"✅ Deleted log file: {file_path}")
            except Exception as e:
                print(f"❌ Failed to delete {file_path}: {e}")


def cleanup_record_files():
    """Clean up record files"""
    print("🧹 Cleaning up record files...")
    
    record_files = [
        "processed_files.txt",
        "cutvideo/processed_files.txt",
        "cutvideo/progress.txt",
        "bilibili_upload_record.txt",
        "upload_record.json",
    ]
    
    for file_path in record_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"✅ Deleted record file: {file_path}")
            except Exception as e:
                print(f"❌ Failed to delete {file_path}: {e}")


def cleanup_optional_tools():
    """Clean up optional tool files"""
    print("🧹 Cleaning up optional tool files...")
    
    optional_files = [
        "ziti.py",
        "picdownload.py", 
        "watermark.py",
        "videomaker.py",
    ]
    
    for file_path in optional_files:
        if Path(file_path).exists():
            response = input(f"Delete {file_path}? (y/N): ")
            if response.lower() == 'y':
                try:
                    Path(file_path).unlink()
                    print(f"✅ Deleted tool file: {file_path}")
                except Exception as e:
                    print(f"❌ Failed to delete {file_path}: {e}")
            else:
                print(f"⏭️  Skipped: {file_path}")


def backup_conf_py():
    """Backup old conf.py file"""
    print("💾 Backing up old configuration file...")
    
    if Path("conf.py").exists():
        backup_dir = Path("backup")
        backup_dir.mkdir(exist_ok=True)
        
        try:
            shutil.copy2("conf.py", backup_dir / "conf.py")
            print("✅ Backed up conf.py to backup/conf.py")
        except Exception as e:
            print(f"❌ Backup failed: {e}")


def cleanup_empty_dirs():
    """Clean up empty directories"""
    print("🧹 Cleaning up empty directories...")
    
    def remove_empty_dirs(path):
        """Recursively delete empty directories"""
        for item in path.iterdir():
            if item.is_dir():
                remove_empty_dirs(item)
        
        try:
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                print(f"✅ Deleted empty directory: {path}")
        except Exception:
            pass
    
    # Clean up empty directories in project root
    for item in Path(".").iterdir():
        if item.is_dir() and item.name not in ["config", "utils", "uploader", "examples", "media", "scripts"]:
            remove_empty_dirs(item)


def show_cleanup_summary():
    """Show cleanup summary"""
    print("\n📊 Cleanup summary:")
    print("✅ Temporary files cleaned")
    print("✅ IDE files cleaned") 
    print("✅ Cache files cleaned")
    print("✅ Log files cleaned")
    print("✅ Record files cleaned")
    print("✅ Empty directories cleaned")
    
    print("\n📋 Suggestions:")
    print("1. Run configuration migration script: python scripts/migrate_config.py")
    print("2. Check backup files in backup/ directory")
    print("3. Restore important configuration files as needed")
    print("4. Test if the project runs normally")


def main():
    """Main function"""
    print("🚀 Starting project cleanup...\n")
    
    # Backup important files
    backup_conf_py()
    
    # Clean up various files
    cleanup_temp_files()
    cleanup_ide_files()
    cleanup_cache_files()
    cleanup_log_files()
    cleanup_record_files()
    cleanup_optional_tools()
    cleanup_empty_dirs()
    
    # Show summary
    show_cleanup_summary()
    
    print("\n🎉 Project cleanup completed!")
    print("📁 Project is now cleaner and suitable for uploading to GitHub")


if __name__ == "__main__":
    main() 