#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONVoyager - Setup Script
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jsonvoyager",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="🚀 JSONVoyager - Interactive Terminal JSON Explorer & Processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/JSONVoyager",
    py_modules=["jsonvoyager"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "jsonvoyager=jsonvoyager:main",
            "jv=jsonvoyager:main",
        ],
    },
    keywords="json cli terminal explorer viewer processor tui interactive",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/JSONVoyager/issues",
        "Source": "https://github.com/gitstq/JSONVoyager",
    },
)
