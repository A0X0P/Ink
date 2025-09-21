"""setup file"""
from setuptools import setup, find_packages

setup(
    name="ink-notes",
    version="0.1.0",
    description="A simple and lightweight CLI tool for note taking.",
    author="a0x0p",
    author_email="1travisxwalker5@gmail.com",
    url="https://github.com/a0x0p/ink",
    license="MIT",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "ink=ink.cli:cli",
        ],
    },
)
