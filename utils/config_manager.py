"""
Configuration Manager
Unified project configuration management, supporting YAML config files and environment variables
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger


class ConfigManager:
    """Configuration Manager"""
    
    def __init__(self, config_file: str = "config/config.yaml"):
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
                logger.info(f"Configuration file loaded successfully: {self.config_file}")
            else:
                logger.warning(f"Configuration file does not exist: {self.config_file}")
                self.config = self.get_default_config()
        except Exception as e:
            logger.error(f"Failed to load configuration file: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "base": {
                "base_dir": ".",
                "log": {
                    "level": "INFO",
                    "file": "logs/sau.log",
                    "max_size": "10MB",
                    "backup_count": 5
                }
            },
            "browser": {
                "chrome_path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "chrome_path_mac": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "chrome_path_linux": "/usr/bin/google-chrome",
                "args": ["--no-sandbox", "--disable-dev-shm-usage"]
            },
            "video": {
                "video_dir": "videos",
                "supported_formats": [".mp4", ".avi", ".mov", ".mkv"],
                "max_file_size": 500,
                "timeout": 300
            },
            "upload": {
                "default_publish_type": 0,
                "default_daily_times": [6, 11, 14, 16, 22],
                "max_uploads_per_day": 5,
                "upload_interval": 30
            },
            "platforms": {
                "douyin": {"enabled": True},
                "tencent": {"enabled": True},
                "bilibili": {"enabled": True},
                "xhs": {"enabled": True},
                "tiktok": {"enabled": True},
                "kuaishou": {"enabled": True}
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value, supports dot-separated key paths"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """Get configuration for specified platform"""
        return self.get(f"platforms.{platform}", {})
    
    def get_browser_path(self) -> str:
        """Get browser path based on operating system"""
        import platform
        system = platform.system().lower()
        
        if system == "darwin":  # macOS
            return self.get("browser.chrome_path_mac", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        elif system == "linux":
            return self.get("browser.chrome_path_linux", "/usr/bin/google-chrome")
        else:  # Windows
            return self.get("browser.chrome_path", "C:/Program Files/Google/Chrome/Application/chrome.exe")
    
    def get_browser_args(self) -> list:
        """Get browser startup arguments"""
        return self.get("browser.args", [])
    
    def is_platform_enabled(self, platform: str) -> bool:
        """Check if platform is enabled"""
        return self.get(f"platforms.{platform}.enabled", False)
    
    def get_cookie_file(self, platform: str) -> str:
        """Get platform cookie file path"""
        return self.get(f"platforms.{platform}.cookie_file", f"cookies/{platform}_uploader/account.json")
    
    def get_title_file(self, platform: str) -> str:
        """Get platform title file path"""
        return self.get(f"platforms.{platform}.title_file", f"{platform}_title_p.txt")
    
    def get_upload_record(self, platform: str) -> str:
        """Get platform upload record file path"""
        return self.get(f"platforms.{platform}.upload_record", f"{platform}_upload_record.json")
    
    def get_platform_settings(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific settings"""
        return self.get(f"platforms.{platform}.settings", {})
    
    def get_proxy_config(self) -> Dict[str, Any]:
        """Get proxy configuration"""
        return self.get("proxy", {})
    
    def get_notification_config(self) -> Dict[str, Any]:
        """Get notification configuration"""
        return self.get("notification", {})
    
    def get_development_config(self) -> Dict[str, Any]:
        """Get development configuration"""
        return self.get("development", {})
    
    def save_config(self):
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"Configuration file saved successfully: {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration file: {e}")
    
    def update_config(self, key: str, value: Any):
        """Update configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.info(f"Configuration updated: {key} = {value}")


# Global configuration manager instance
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """Get global configuration manager"""
    return config_manager


def get_env_config(key: str, default: Any = None) -> Any:
    """Get configuration from environment variables, priority higher than config file"""
    env_key = f"SAU_{key.upper().replace('.', '_')}"
    return os.getenv(env_key, default)


def get_config_value(key: str, default: Any = None) -> Any:
    """Get configuration value, prioritize environment variables"""
    env_value = get_env_config(key)
    if env_value is not None:
        return env_value
    return config_manager.get(key, default) 