#!/usr/bin/env python
from setuptools import find_packages, setup

from coinbase import __source__, __version__

issues_url = f"{__source__}/issues"
documentation_url = f"{__source__}/tree/main/docs"
download_url = (
    f"{__source__}/releases/download/{__version__}/coinbase-{__version__}.tar.gz"
)
description_file = "README.md"

with open(description_file, "r") as file:
    long_description = file.read()

setup(
    name="coinbase",
    version=__version__,
    author="teleprint-me",
    author_email="noreply@teleprint.me",
    license="AGPL",
    url=__source__,
    download_url=download_url,
    project_urls={
        "Issues": issues_url,
        "Documentation": documentation_url,
    },
    python_requires=">=3.8",
    install_requires=["requests>=2.27.1"],
    tests_require=[
        "dateutils>=0.6.12",
        "pytest>=6.2.5",
        "requests>=2.27.1",
    ],
    packages=find_packages(where="."),
    description="Another Unofficial Python Wrapper for Coinbase",
    description_file=description_file,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "requests",
        "wrapper",
        "rest",
        "api",
        "trading",
        "client",
        "crypto",
        "currency",
        "coinbase",
        "exchange",
    ],
    classifiers=[
        "Development Status :: 4 - Development/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: AGPL License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
