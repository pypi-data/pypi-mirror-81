#!/usr/bin/env python3

from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

setuptools.setup(
    name="urinterface",
    version="0.0.5",
    description="UR Robot Interface",
    # Allow UTF-8 characters in README with encoding argument.
    long_description=project_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords=["python", "ur robot", "universal robot"],
    author="Claudio Gomes and Emil Madsen",
    author_email="claudio.gomes@eng.au.dk",
    url="https://gitlab.au.dk/clagms/urinterface",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    license="INTOCPS",
    license_files=["LICENSE"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
