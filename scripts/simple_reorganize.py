#!/usr/bin/env python3
"""
Simplified Project Reorganization Script
First organize the most chaotic parts to make the project clearer
"""

import os
import shutil
from pathlib import Path


def create_basic_structure():
    """Create basic directory structure"""
    print("📁 Creating basic directory structure...")
    
    basic_dirs = [
        "tools",                 # Tool scripts
        "tools/cookie_manager",   # Cookie management tools
        "tools/upload_tools",     # Upload tools
        "tools/video_processing", # Video processing tools
        "data",                  # Data files
        "data/cookies",          # Cookie storage
        "data/logs",             # Log files
        "data/records",          # Record files
        "data/titles",           # Title files
        "data/videos",           # Video files
        "assets",                # Resource files
        "assets/media",          # Media files
        "docs",                  # Documentation
    ]
    
    for dir_path in basic_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")


def move_tool_files():
    """Move tool files"""
    print("\n🛠️  Moving tool files...")
    
    # Cookie management tools
    cookie_tools = [
        "get_douyin_cookie.py",
        "get_tencent_cookie.py", 
        "get_bilibili_cookie.py",
        "get_tk_cookie.py",
    ]
    
    for tool in cookie_tools:
        if Path(tool).exists():
            try:
                shutil.move(tool, "tools/cookie_manager/")
                print(f"✅ Moved: {tool} -> tools/cookie_manager/")
            except Exception as e:
                print(f"❌ Failed to move {tool}: {e}")
    
    # Upload tools
    upload_tools = [
        "upload_video_to_douyin.py",
        "upload_video_to_bilibili.py",
        "upload_video_to_tiktok.py",
    ]
    
    for tool in upload_tools:
        if Path(tool).exists():
            try:
                shutil.move(tool, "tools/upload_tools/")
                print(f"✅ Moved: {tool} -> tools/upload_tools/")
            except Exception as e:
                print(f"❌ Failed to move {tool}: {e}")
    
    # Video processing tools
    video_tools = [
        "videomaker.py",
        "ziti.py",
        "watermark.py",
        "picdownload.py",
    ]
    
    for tool in video_tools:
        if Path(tool).exists():
            try:
                shutil.move(tool, "tools/video_processing/")
                print(f"✅ Moved: {tool} -> tools/video_processing/")
            except Exception as e:
                print(f"❌ Failed to move {tool}: {e}")


def move_cutvideo_files():
    """Move files from cutvideo directory"""
    print("\n🎬 Moving video processing files...")
    
    if Path("cutvideo").exists():
        cutvideo_files = [
            "cutvideo/cutvideo.py",
            "cutvideo/cutvideobak.py",
            "cutvideo/videomakerp_dy.py",
        ]
        
        for file_path in cutvideo_files:
            if Path(file_path).exists():
                try:
                    shutil.move(file_path, "tools/video_processing/")
                    print(f"✅ Moved: {file_path} -> tools/video_processing/")
                except Exception as e:
                    print(f"❌ Failed to move {file_path}: {e}")
        
        # Delete empty cutvideo directory
        try:
            if not any(Path("cutvideo").iterdir()):
                shutil.rmtree("cutvideo")
                print("✅ Deleted empty directory: cutvideo")
        except Exception as e:
            print(f"❌ Failed to delete cutvideo directory: {e}")


def move_data_files():
    """Move data files"""
    print("\n📊 Moving data files...")
    
    # Move existing directories
    data_dirs = {
        "cookies": "data/cookies",
        "logs": "data/logs", 
        "videos": "data/videos",
        "media": "assets/media",
    }
    
    for src, dst in data_dirs.items():
        if Path(src).exists():
            try:
                if Path(dst).exists():
                    # Merge directory contents
                    for item in Path(src).iterdir():
                        shutil.move(str(item), dst)
                    shutil.rmtree(src)
                else:
                    shutil.move(src, dst)
                print(f"✅ Moved: {src} -> {dst}")
            except Exception as e:
                print(f"❌ Failed to move {src}: {e}")
    
    # Move record files
    record_files = [
        "bilibili_upload_record.txt",
        "upload_record.json",
        "processed_files.txt",
        "video_processing.log",
    ]
    
    for file_path in record_files:
        if Path(file_path).exists():
            try:
                shutil.move(file_path, "data/records/")
                print(f"✅ Moved: {file_path} -> data/records/")
            except Exception as e:
                print(f"❌ Failed to move {file_path}: {e}")
    
    # Move title files
    title_files = [
        "bilibili_title_p.txt",
        "douyin_title_p.txt", 
        "bilibili_title.txt",
    ]
    
    for file_path in title_files:
        if Path(file_path).exists():
            try:
                shutil.move(file_path, "data/titles/")
                print(f"✅ Moved: {file_path} -> data/titles/")
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
    
    # Move examples directory
    if Path("examples").exists():
        try:
            shutil.move("examples", "docs/examples")
            print("✅ Moved: examples -> docs/examples")
        except Exception as e:
            print(f"❌ Failed to move examples: {e}")


def create_init_files():
    """Create __init__.py files"""
    print("\n📄 Creating __init__.py files...")
    
    init_dirs = [
        "tools",
        "tools/cookie_manager",
        "tools/upload_tools", 
        "tools/video_processing",
        "data",
        "data/cookies",
        "data/logs",
        "data/records",
        "data/titles",
        "data/videos",
        "assets",
        "assets/media",
        "docs",
    ]
    
    for dir_path in init_dirs:
        init_file = Path(dir_path) / "__init__.py"
        init_file.touch()
        print(f"✅ Created: {init_file}")


def create_structure_doc():
    """Create simplified structure documentation"""
    print("\n📋 Creating structure documentation...")
    
    doc = """# Simplified Project Structure

## 📁 Current Directory Structure

```
social-auto-upload/
├── src/                    # Source code (keep as is)
│   ├── core/              # Core functionality
│   ├── platforms/         # Platform implementations
│   ├── utils/             # Utility modules
│   └── config/            # Configuration management
├── tools/                 # Tool scripts
│   ├── cookie_manager/    # Cookie management tools
│   ├── upload_tools/      # Upload tools
│   └── video_processing/  # Video processing tools
├── data/                  # Data files
│   ├── cookies/           # Cookie storage
│   ├── logs/              # Log files
│   ├── records/           # Record files
│   ├── titles/            # Title files
│   └── videos/            # Video files
├── assets/                # Resource files
│   └── media/             # Media files
├── docs/                  # Documentation
│   ├── README.MD
│   ├── QUICKSTART.md
│   ├── CHANGELOG.md
│   ├── LICENSE
│   └── examples/          # Usage examples
├── scripts/               # Project scripts
├── requirements.txt       # Dependencies file
├── setup.py              # Installation configuration
└── .gitignore            # Git ignore file
```

## 🎯 Organization Results

✅ **Tool file categorization**: Tool files categorized by functionality
✅ **Data file centralization**: All runtime data centrally managed
✅ **Documentation organization**: Documentation files unified storage
✅ **Clear structure**: Directory structure more clear and understandable

## 📝 Usage Instructions

1. **Cookie management**: `tools/cookie_manager/`
2. **Upload tools**: `tools/upload_tools/`
3. **Video processing**: `tools/video_processing/`
4. **Data storage**: Corresponding subdirectories under `data/`
5. **Documentation**: `docs/` directory

## 🔄 Next Steps

1. Update import paths in code
2. Test if tools work normally
3. Further optimize structure as needed
"""
    
    with open("docs/SIMPLE_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write(doc)
    
    print("✅ Created structure documentation: docs/SIMPLE_STRUCTURE.md")


def main():
    """Main function"""
    print("🚀 Starting simplified project reorganization...\n")
    
    # Create basic structure
    create_basic_structure()
    
    # Move files
    move_tool_files()
    move_cutvideo_files()
    move_data_files()
    move_documentation()
    
    # Create initialization files
    create_init_files()
    
    # Create documentation
    create_structure_doc()
    
    print("\n🎉 Simplified reorganization completed!")
    print("\n📋 Organization results:")
    print("✅ Tool files categorized by functionality")
    print("✅ Data files centrally managed")
    print("✅ Documentation files unified storage")
    print("✅ Directory structure clearer")
    
    print("\n📝 Next steps:")
    print("1. Check if tools work normally")
    print("2. Update path references in code")
    print("3. Test project functionality")


if __name__ == "__main__":
    main() 