#!/usr/bin/env python3
"""
Project Reorganization Script
Organize project directory structure to make it clearer and more professional
"""

import os
import shutil
from pathlib import Path


def create_new_structure():
    """Create new directory structure"""
    print("📁 Creating new directory structure...")
    
    # Main directories
    main_dirs = [
        "src",                    # Source code directory
        "src/core",              # Core functionality
        "src/platforms",         # Platform implementations
        "src/utils",             # Utility modules
        "src/config",            # Configuration management
        "tools",                 # Tool scripts
        "tools/video_processing", # Video processing tools
        "tools/cookie_manager",   # Cookie management tools
        "docs",                  # Documentation
        "tests",                 # Tests
        "assets",                # Resource files
        "assets/media",          # Media files
        "assets/templates",      # Template files
        "data",                  # Data files
        "data/cookies",          # Cookie storage
        "data/logs",             # Log files
        "data/records",          # Record files
        "data/titles",           # Title files
        "data/videos",           # Video files
    ]
    
    for dir_path in main_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")


def move_core_files():
    """Move core files"""
    print("\n📦 Moving core files...")
    
    # Core file mappings
    core_files = {
        "cli_main.py": "src/core/",
        "conf.py": "src/config/",
        "utils/config_manager.py": "src/config/",
        "utils/base_social_media.py": "src/utils/",
        "utils/constant.py": "src/utils/",
        "utils/files_times.py": "src/utils/",
        "utils/log.py": "src/utils/",
        "utils/stealth.min.js": "src/utils/",
    }
    
    for src, dst in core_files.items():
        if Path(src).exists():
            try:
                shutil.move(src, dst)
                print(f"✅ Moved: {src} -> {dst}")
            except Exception as e:
                print(f"❌ Failed to move {src}: {e}")


def move_platform_files():
    """Move platform-related files"""
    print("\n🌐 Moving platform files...")
    
    # Platform file mappings
    platform_files = {
        "uploader/douyin_uploader/": "src/platforms/douyin/",
        "uploader/tencent_uploader/": "src/platforms/tencent/",
        "uploader/bilibili_uploader/": "src/platforms/bilibili/",
        "uploader/xhs_uploader/": "src/platforms/xhs/",
        "uploader/tk_uploader/": "src/platforms/tiktok/",
        "uploader/ks_uploader/": "src/platforms/kuaishou/",
    }
    
    for src, dst in platform_files.items():
        if Path(src).exists():
            try:
                if Path(dst).exists():
                    shutil.rmtree(dst)
                shutil.move(src, dst)
                print(f"✅ Moved: {src} -> {dst}")
            except Exception as e:
                print(f"❌ Failed to move {src}: {e}")


def move_tool_files():
    """Move tool files"""
    print("\n🛠️  Moving tool files...")
    
    # Tool file mappings
    tool_files = {
        "get_douyin_cookie.py": "tools/cookie_manager/",
        "get_tencent_cookie.py": "tools/cookie_manager/",
        "get_bilibili_cookie.py": "tools/cookie_manager/",
        "get_tk_cookie.py": "tools/cookie_manager/",
        "upload_video_to_douyin.py": "tools/upload_tools/",
        "upload_video_to_bilibili.py": "tools/upload_tools/",
        "upload_video_to_tiktok.py": "tools/upload_tools/",
        "videomaker.py": "tools/video_processing/",
        "ziti.py": "tools/video_processing/",
        "watermark.py": "tools/video_processing/",
        "picdownload.py": "tools/video_processing/",
    }
    
    # Create tool subdirectories
    Path("tools/upload_tools").mkdir(exist_ok=True)
    
    for src, dst in tool_files.items():
        if Path(src).exists():
            try:
                shutil.move(src, dst)
                print(f"✅ Moved: {src} -> {dst}")
            except Exception as e:
                print(f"❌ Failed to move {src}: {e}")


def move_video_processing():
    """Move video processing related files"""
    print("\n🎬 Moving video processing files...")
    
    # Move cutvideo directory contents
    if Path("cutvideo").exists():
        try:
            # Move files
            cutvideo_files = [
                "cutvideo/cutvideo.py",
                "cutvideo/cutvideobak.py", 
                "cutvideo/videomakerp_dy.py"
            ]
            
            for file_path in cutvideo_files:
                if Path(file_path).exists():
                    shutil.move(file_path, "tools/video_processing/")
                    print(f"✅ Moved: {file_path} -> tools/video_processing/")
            
            # Delete empty cutvideo directory
            if not any(Path("cutvideo").iterdir()):
                shutil.rmtree("cutvideo")
                print("✅ Deleted empty directory: cutvideo")
                
        except Exception as e:
            print(f"❌ Failed to move video processing files: {e}")


def move_data_files():
    """Move data files"""
    print("\n📊 Moving data files...")
    
    # Data file mappings
    data_files = {
        "cookies/": "data/cookies/",
        "logs/": "data/logs/",
        "videos/": "data/videos/",
        "media/": "assets/media/",
    }
    
    for src, dst in data_files.items():
        if Path(src).exists():
            try:
                if Path(dst).exists():
                    # Merge directory contents
                    for item in Path(src).iterdir():
                        if item.is_file():
                            shutil.move(str(item), dst)
                        elif item.is_dir():
                            shutil.move(str(item), dst)
                    shutil.rmtree(src)
                else:
                    shutil.move(src, dst)
                print(f"✅ Moved: {src} -> {dst}")
            except Exception as e:
                print(f"❌ Failed to move {src}: {e}")


def move_record_files():
    """Move record files"""
    print("\n📝 Moving record files...")
    
    record_files = [
        "bilibili_upload_record.txt",
        "upload_record.json", 
        "processed_files.txt",
        "video_processing.log",
        "bilibili_title_p.txt",
        "douyin_title_p.txt",
        "bilibili_title.txt",
    ]
    
    for file_path in record_files:
        if Path(file_path).exists():
            try:
                if file_path.endswith(('.txt', '.json')):
                    if 'title' in file_path:
                        shutil.move(file_path, "data/titles/")
                        print(f"✅ Moved: {file_path} -> data/titles/")
                    elif 'record' in file_path or 'processed' in file_path:
                        shutil.move(file_path, "data/records/")
                        print(f"✅ Moved: {file_path} -> data/records/")
                    elif 'log' in file_path:
                        shutil.move(file_path, "data/logs/")
                        print(f"✅ Moved: {file_path} -> data/logs/")
            except Exception as e:
                print(f"❌ Failed to move {file_path}: {e}")


def move_documentation():
    """Move documentation files"""
    print("\n📚 Moving documentation files...")
    
    doc_files = [
        "README.MD",
        "QUICKSTART.md", 
        "CHANGELOG.md",
        "LICENSE",
    ]
    
    for file_path in doc_files:
        if Path(file_path).exists():
            try:
                shutil.move(file_path, "docs/")
                print(f"✅ Moved: {file_path} -> docs/")
            except Exception as e:
                print(f"❌ Failed to move {file_path}: {e}")


def move_examples():
    """Move example files"""
    print("\n💡 Moving example files...")
    
    if Path("examples").exists():
        try:
            shutil.move("examples", "docs/examples")
            print("✅ Moved: examples -> docs/examples")
        except Exception as e:
            print(f"❌ Failed to move examples: {e}")


def create_new_main_files():
    """Create new main files"""
    print("\n📄 Creating new main files...")
    
    # Create new __init__.py files
    init_files = [
        "src/__init__.py",
        "src/core/__init__.py",
        "src/platforms/__init__.py",
        "src/utils/__init__.py",
        "src/config/__init__.py",
        "tools/__init__.py",
        "tools/video_processing/__init__.py",
        "tools/cookie_manager/__init__.py",
        "tools/upload_tools/__init__.py",
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"✅ Created: {init_file}")


def create_new_config():
    """Create new configuration files"""
    print("\n⚙️  Creating new configuration files...")
    
    # Move configuration files
    if Path("config/config.yaml").exists():
        try:
            shutil.move("config/config.yaml", "src/config/config.yaml")
            shutil.move("config/config.example.yaml", "src/config/config.example.yaml")
            print("✅ Moved configuration files to src/config/")
        except Exception as e:
            print(f"❌ Failed to move configuration files: {e}")


def update_imports():
    """Update import paths"""
    print("\n🔧 Updating import paths...")
    
    # Here you can add logic to automatically update import paths
    # Since it's complex, manual checking and updating is recommended
    print("⚠️  Please manually check and update import paths in code")


def create_project_structure_doc():
    """Create project structure documentation"""
    print("\n📋 Creating project structure documentation...")
    
    structure_doc = """# Project Structure Documentation

## 📁 Directory Structure

```
social-auto-upload/
├── src/                    # Source code directory
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   └── cli_main.py    # Command line main program
│   ├── platforms/         # Platform implementations
│   │   ├── __init__.py
│   │   ├── douyin/        # Douyin platform
│   │   ├── tencent/       # Tencent video platform
│   │   ├── bilibili/      # Bilibili platform
│   │   ├── xhs/           # Xiaohongshu platform
│   │   ├── tiktok/        # TikTok platform
│   │   └── kuaishou/      # Kuaishou platform
│   ├── utils/             # Utility modules
│   │   ├── __init__.py
│   │   ├── base_social_media.py
│   │   ├── constant.py
│   │   ├── files_times.py
│   │   ├── log.py
│   │   └── stealth.min.js
│   └── config/            # Configuration management
│       ├── __init__.py
│       ├── config_manager.py
│       ├── config.yaml
│       └── config.example.yaml
├── tools/                 # Tool scripts
│   ├── __init__.py
│   ├── video_processing/  # Video processing tools
│   │   ├── __init__.py
│   │   ├── cutvideo.py
│   │   ├── videomaker.py
│   │   ├── watermark.py
│   │   └── ziti.py
│   ├── cookie_manager/    # Cookie management tools
│   │   ├── __init__.py
│   │   ├── get_douyin_cookie.py
│   │   ├── get_tencent_cookie.py
│   │   ├── get_bilibili_cookie.py
│   │   └── get_tk_cookie.py
│   └── upload_tools/      # Upload tools
│       ├── __init__.py
│       ├── upload_video_to_douyin.py
│       ├── upload_video_to_bilibili.py
│       └── upload_video_to_tiktok.py
├── docs/                  # Documentation
│   ├── README.MD
│   ├── QUICKSTART.md
│   ├── CHANGELOG.md
│   ├── LICENSE
│   └── examples/          # Usage examples
├── assets/                # Resource files
│   ├── media/             # Media files
│   └── templates/         # Template files
├── data/                  # Data files
│   ├── cookies/           # Cookie storage
│   ├── logs/              # Log files
│   ├── records/           # Record files
│   ├── titles/            # Title files
│   └── videos/            # Video files
├── tests/                 # Tests
├── scripts/               # Project scripts
│   ├── init_project.py
│   ├── migrate_config.py
│   ├── cleanup_project.py
│   ├── quick_cleanup.py
│   └── reorganize_project.py
├── requirements.txt       # Dependencies file
├── setup.py              # Installation configuration
└── .gitignore            # Git ignore file
```

## 🔧 Main Module Descriptions

### src/core/
Core functionality module, containing command line interface and main business logic.

### src/platforms/
Implementations for various social media platforms, one subdirectory per platform.

### src/utils/
Common utility modules, containing base classes, constants, file processing, etc.

### src/config/
Configuration management module, unified project configuration management.

### tools/
Various tool scripts, categorized by functionality.

### docs/
Project documentation and usage examples.

### data/
Runtime data storage, containing cookies, logs, records, etc.

### assets/
Static resource files, such as media files and templates.

## 📝 Usage Instructions

1. **Develop new features**: Add code in the `src/` directory
2. **Add new platforms**: Create new directories in `src/platforms/`
3. **Add tools**: Add to `tools/` directory categorized by functionality
4. **Manage configuration**: Use the configuration manager in `src/config/`
5. **Store data**: Place runtime data in the `data/` directory

## 🔄 Migration Notes

After project reorganization, the following content needs to be updated:
1. Import paths
2. Configuration file paths
3. Relative path references
4. Path descriptions in documentation
"""
    
    with open("docs/PROJECT_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write(structure_doc)
    
    print("✅ Created project structure documentation: docs/PROJECT_STRUCTURE.md")


def main():
    """Main function"""
    print("🚀 Starting project structure reorganization...\n")
    
    # Create new structure
    create_new_structure()
    
    # Move files
    move_core_files()
    move_platform_files()
    move_tool_files()
    move_video_processing()
    move_data_files()
    move_record_files()
    move_documentation()
    move_examples()
    
    # Create new files
    create_new_main_files()
    create_new_config()
    
    # Create documentation
    create_project_structure_doc()
    
    # Update imports
    update_imports()
    
    print("\n🎉 Project reorganization completed!")
    print("\n📋 Next steps:")
    print("1. Check and update import paths in code")
    print("2. Test if the project runs normally")
    print("3. Update path descriptions in documentation")
    print("4. Run tests to ensure functionality is normal")


if __name__ == "__main__":
    main() 