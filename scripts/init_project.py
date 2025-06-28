#!/usr/bin/env python3
"""
Project Initialization Script
Used to create necessary directory structure and configuration files
"""

import os
import shutil
from pathlib import Path
from utils.config_manager import ConfigManager


def create_directories():
    """Create necessary directory structure"""
    directories = [
        "config",
        "cookies",
        "cookies/douyin_uploader",
        "cookies/tencent_uploader", 
        "cookies/bilibili_uploader",
        "cookies/tk_uploader",
        "cookies/ks_uploader",
        "videos",
        "logs",
        "media",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def create_config_files():
    """Create configuration files"""
    # Copy configuration example file
    if not Path("config/config.yaml").exists():
        if Path("config/config.example.yaml").exists():
            shutil.copy("config/config.example.yaml", "config/config.yaml")
            print("✅ Created configuration file: config/config.yaml")
        else:
            print("⚠️  Configuration example file does not exist, please create configuration file manually")


def create_title_files():
    """Create title file templates"""
    title_files = [
        "douyin_title_p.txt",
        "tencent_title_p.txt", 
        "bilibili_title_p.txt",
        "xhs_title_p.txt",
        "tiktok_title_p.txt",
        "kuaishou_title_p.txt"
    ]
    
    for title_file in title_files:
        if not Path(title_file).exists():
            with open(title_file, 'w', encoding='utf-8') as f:
                f.write("# Title template file\n")
                f.write("# One title per line, supports emoji and hashtags\n")
                f.write("# Examples:\n")
                f.write("# This is an example title 🎬\n")
                f.write("# Another title #hashtag #shortvideo\n")
            print(f"✅ Created title file: {title_file}")


def create_upload_record_files():
    """Create upload record files"""
    record_files = [
        "upload_record.json",
        "bilibili_upload_record.txt",
        "tencent_upload_record.json",
        "xhs_upload_record.json",
        "tiktok_upload_record.json",
        "kuaishou_upload_record.json"
    ]
    
    for record_file in record_files:
        if not Path(record_file).exists():
            if record_file.endswith('.json'):
                with open(record_file, 'w', encoding='utf-8') as f:
                    f.write('[]')
            else:
                with open(record_file, 'w', encoding='utf-8') as f:
                    f.write('# Upload record file\n')
            print(f"✅ Created record file: {record_file}")


def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
build/
dist/
*.egg-info/

# Virtual environments
.env
.venv
env/
venv/

# IDE
.idea/
.vscode/

# Logs
logs/
*.log

# Cookies and sensitive data
cookies/
config/config.yaml

# Video files
videos/
*.mp4
*.avi
*.mov
*.mkv

# Upload records
*_upload_record.txt
*_upload_record.json
upload_record.json

# Title files
*_title.txt
*_title_p.txt

# Temporary files
temp_*
fadein_*
output.mp4
test_output*.mp4

# System files
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore file")


def check_dependencies():
    """Check dependencies"""
    print("\n🔍 Checking dependencies...")
    
    try:
        import playwright
        print("✅ playwright is installed")
    except ImportError:
        print("❌ playwright is not installed, please run: pip install playwright")
        print("   Then run: playwright install chromium firefox")
    
    try:
        import yaml
        print("✅ pyyaml is installed")
    except ImportError:
        print("❌ pyyaml is not installed, please run: pip install pyyaml")
    
    try:
        import loguru
        print("✅ loguru is installed")
    except ImportError:
        print("❌ loguru is not installed, please run: pip install loguru")


def main():
    """Main function"""
    print("🚀 Starting Social Auto Upload project initialization...\n")
    
    # Create directory structure
    print("📁 Creating directory structure...")
    create_directories()
    
    # Create configuration files
    print("\n⚙️  Creating configuration files...")
    create_config_files()
    
    # Create title files
    print("\n📝 Creating title files...")
    create_title_files()
    
    # Create upload record files
    print("\n📊 Creating upload record files...")
    create_upload_record_files()
    
    # Create .gitignore file
    print("\n🔒 Creating .gitignore file...")
    create_gitignore()
    
    # Check dependencies
    check_dependencies()
    
    print("\n🎉 Project initialization completed!")
    print("\n📋 Next steps:")
    print("1. Edit config/config.yaml configuration file")
    print("2. Set Chrome browser path")
    print("3. Get cookies for each platform")
    print("4. Prepare video files and titles")
    print("5. Start using!")
    
    print("\n📖 For detailed usage instructions, please check the README.MD file")


if __name__ == "__main__":
    main() 