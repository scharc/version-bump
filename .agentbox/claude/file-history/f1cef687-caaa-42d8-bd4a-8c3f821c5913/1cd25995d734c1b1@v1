#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="my-python-project",
    version="1.2.3",
    description="A sample Python project",
    author="Test Author",
    author_email="test@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "mypy"],
    },
)
