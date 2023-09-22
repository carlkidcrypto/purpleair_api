#!/usr/bin/env python3
from setuptools import setup
import os


def read_file(filename):
    with open(
        os.path.join(os.path.dirname(__file__), filename), encoding="utf-8"
    ) as file:
        return file.read()


setup(
    name="purpleair_api",
    version="1.1.1",
    license="MIT",
    author="Carlos Santos",
    author_email="dose.lucky.sake@cloak.id",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    packages=["purpleair_api"],
    url="https://github.com/carlkidcrypto/purpleair_api",
    keywords=["purpleair_api", "purple air api", "purple_air", "purple air"],
    install_requires=["requests"],
    platforms=["Windows 32/64", "Linux 32/64", "MacOS 32/64"],
)
