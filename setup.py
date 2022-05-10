#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="main",
    version="1.0",
    packages=find_packages(),
    scripts=["src/run.py"],
    author="mschneider",
    author_email="markus.schneider@rwu.de",
)
