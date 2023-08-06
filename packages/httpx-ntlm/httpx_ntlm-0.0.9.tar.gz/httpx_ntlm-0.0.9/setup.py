#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="httpx_ntlm",
    version="0.0.9",
    packages=["httpx_ntlm"],
    install_requires=["httpx>=0.15.*", "ntlm-auth==1.5.*", "cryptography==3.1.*"],
    provides=["httpx_ntlm"],
    author="Ludovic VAUGEOIS",
    author_email="ulodciv@gmail.com",
    url="https://github.com/ulodciv/httpx-ntlm",
    description="This package allows for HTTP NTLM authentication using the HTTPX library.",
    license="ISC",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
)
