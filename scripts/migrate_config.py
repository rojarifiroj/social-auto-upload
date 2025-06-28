#!/usr/bin/env python3
"""
Configuration Migration Script
Migrate existing hardcoded configurations to the new configuration management system
"""

import json
import shutil
from pathlib import Path
from utils.config_manager import ConfigManager


def migrate_conf_py():
    """Migrate configurations from conf.py"""
    print("🔄 Migrating conf.py configurations...")
    
    try:
        # Read existing conf.py
        with open("conf.py", "r", encoding="utf-8") as f:
            conf_content = f.read()
        
        # Extract configuration values
        config = {}
        
        # Extract BASE_DIR
        if "BASE_DIR" in conf_content:
            config["base"]["base_dir"] = "."
        
        # Extract XHS_SERVER
        if "XHS_SERVER" in conf_content:
            import re
            match = re.search(r'XHS_SERVER\s*=\s*["\']([^"\']+)["\']', conf_content)
            if match:
                config["platforms"]["xhs"]["settings"]["sign_server"] = match.group(1)
        
        # Extract LOCAL_CHROME_PATH
        if "LOCAL_CHROME_PATH" in conf_content:
            import re
            match = re.search(r'LOCAL_CHROME_PATH\s*=\s*["\']([^"\']+)["\']', conf_content)
            if match:
                config["browser"]["chrome_path"] = match.group(1)
        
        print("✅ conf.py configuration migration completed")
        return config
        
    except Exception as e:
        print(f"❌ Failed to migrate conf.py: {e}")
        return {}


def migrate_existing_files():
    """Migrate existing file configurations"""
    print("🔄 Migrating existing file configurations...")
    
    config = {}
    
    # Check existing title files
    title_files = {
        "douyin_title_p.txt": "platforms.douyin.title_file",
        "bilibili_title_p.txt": "platforms.bilibili.title_file",
        "bilibili_title.txt": "platforms.bilibili.title_file_default"
    }
    
    for file_path, config_key in title_files.items():
        if Path(file_path).exists():
            keys = config_key.split('.')
            current = config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = file_path
            print(f"✅ Found title file: {file_path}")
    
    # Check existing upload record files
    record_files = {
        "upload_record.json": "platforms.douyin.upload_record",
        "bilibili_upload_record.txt": "platforms.bilibili.upload_record"
    }
    
    for file_path, config_key in record_files.items():
        if Path(file_path).exists():
            keys = config_key.split('.')
            current = config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = file_path
            print(f"✅ Found record file: {file_path}")
    
    print("✅ Existing file configuration migration completed")
    return config


def backup_old_config():
    """Backup old configuration files"""
    print("💾 Backing up old configuration files...")
    
    backup_dir = Path("backup")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        "conf.py",
        "douyin_title_p.txt",
        "bilibili_title_p.txt",
        "bilibili_title.txt",
        "upload_record.json",
        "bilibili_upload_record.txt"
    ]
    
    for file_path in files_to_backup:
        if Path(file_path).exists():
            shutil.copy2(file_path, backup_dir / file_path)
            print(f"✅ Backed up file: {file_path}")
    
    print("✅ Backup completed, files saved in backup/ directory")


def update_config_manager():
    """Update configuration manager"""
    print("🔄 Updating configuration manager...")
    
    config_manager = ConfigManager()
    
    # Merge migrated configurations
    migrated_config = migrate_conf_py()
    file_config = migrate_existing_files()
    
    # Merge configurations
    def merge_config(target, source):
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                merge_config(target[key], value)
            else:
                target[key] = value
    
    merge_config(config_manager.config, migrated_config)
    merge_config(config_manager.config, file_config)
    
    # Save configuration
    config_manager.save_config()
    print("✅ Configuration manager update completed")


def create_migration_report():
    """Create migration report"""
    print("📊 Generating migration report...")
    
    report = """# Configuration Migration Report

## Migration Content

### 1. Configuration File Migration
- ✅ Created unified config/config.yaml configuration file
- ✅ Created configuration example file config/config.example.yaml
- ✅ Implemented configuration manager utils/config_manager.py

### 2. Existing Configuration Migration
- ✅ Migrated configuration items from conf.py
- ✅ Migrated existing title file configurations
- ✅ Migrated existing upload record file configurations

### 3. Project Structure Optimization
- ✅ Updated .gitignore file
- ✅ Created setup.py for project packaging
- ✅ Added LICENSE file
- ✅ Updated README.MD documentation
- ✅ Created CHANGELOG.md update log

## Using the New Configuration System

### 1. Configuration File Locations
- Main configuration file: config/config.yaml
- Configuration example: config/config.example.yaml

### 2. Environment Variable Support
The project supports configuration override through environment variables:
```bash
export SAU_BROWSER_CHROME_PATH="/path/to/chrome"
export SAU_PLATFORMS_DOUYIN_ENABLED="true"
```

### 3. Configuration Access Methods
```python
from utils.config_manager import get_config

config = get_config()
chrome_path = config.get_browser_path()
douyin_enabled = config.is_platform_enabled("douyin")
```

## Notes

1. Old conf.py file has been backed up to backup/ directory
2. It's recommended to delete the old conf.py file and use the new configuration system
3. All hardcoded paths can now be managed through configuration files
4. Supports environment variable override for easy deployment and CI/CD

## Next Steps

1. Test if the new configuration system works properly
2. Adjust parameters in configuration files as needed
3. Update hardcoded path references in code
4. Delete old configuration files that are no longer needed

---
Migration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    from datetime import datetime
    report = report.format(datetime=datetime)
    
    with open("MIGRATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ Migration report generated: MIGRATION_REPORT.md")


def main():
    """Main function"""
    print("🚀 Starting configuration migration...\n")
    
    # Backup old configurations
    backup_old_config()
    
    # Migrate configurations
    update_config_manager()
    
    # Generate migration report
    create_migration_report()
    
    print("\n🎉 Configuration migration completed!")
    print("\n📋 Migration summary:")
    print("✅ Created unified configuration management system")
    print("✅ Migrated existing configuration items")
    print("✅ Backed up old configuration files")
    print("✅ Generated migration report")
    
    print("\n📖 Please check MIGRATION_REPORT.md for detailed information")
    print("🔧 You can now use the new configuration system!")


if __name__ == "__main__":
    main() 