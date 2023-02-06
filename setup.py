#! /usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="canonicalwebteam.store-base",
    version="0.1.0",
    author="Canonical webteam",
    author_email="webteam@canonical.com",
    url=(
        "https://github.com/canonical-web-and-design/"
        "canonicalwebteam.store-base"
    ),
    description=(
        "Flask extension to integrate discourse content generated "
        "to docs to your website."
    ),
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "python=3.8",
        "canonicalwebteam.flask-base=1.0.6",
        "canonicalwebteam.image-template=1.3.1",
        "canonicalwebteam.store-api=4.0.0",
        "canonicalwebteam.blog=6.4.0",
        "canonicalwebteam.candid=0.9.0",
        "canonicalwebteam.discourse=5.0.3",
        "Flask-WTF=1.0.1",
        "humanize=3.13.1",
        "mistune=2.0.4",
        "pybadges=3.0.0",
        "pymacaroons=0.13.0",
        "ruamel.yaml=0.17.21",
        "pipenv=2022.12.19",
        "python-dotenv=0.21.1" ,  
    ],
    tests_require=[
        "vcrpy-unittest",
        "httpretty",
    ],
)