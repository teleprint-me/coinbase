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
    install_requires=[
        "attrs==21.4.0",
        "build==0.7.0",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.12",
        "dateutils==0.6.12",
        "idna==3.3",
        "iniconfig==1.1.1",
        "packaging==21.3",
        "pep517==0.12.0",
        "pluggy==1.0.0",
        "py==1.11.0",
        "pyparsing==3.0.7",
        "pytest==6.2.5",
        "python-dateutil==2.8.2",
        "pytz==2021.3",
        "requests==2.27.1",
        "six==1.16.0",
        "toml==0.10.2",
        "tomli==2.0.1",
        "urllib3==1.26.8",
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
