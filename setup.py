"""
Social Auto Upload - Social Media Auto Upload Tool
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.MD", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements file
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="social-auto-upload",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated tool for publishing videos to various social media platforms",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rojarifiroj/social-auto-upload",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "sau=cli_main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.txt", "*.js"],
    },
    keywords="social media, video upload, automation, douyin, tiktok, bilibili, xiaohongshu",
    project_urls={
        "Bug Reports": "https://github.com/rojarifiroj/social-auto-upload/issues",
        "Source": "https://github.com/rojarifiroj/social-auto-upload",
        "Documentation": "https://github.com/rojarifiroj/social-auto-upload#readme",
    },
) 