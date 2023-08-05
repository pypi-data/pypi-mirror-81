# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('urigui/uricli.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="urigui",
    packages=["urigui"],
    entry_points={
        "console_scripts": ['uri = urigui.uricli:main']
    },
    version=version,
    description="Utility CLI for submitting solutions to URI Online Judge.",
    long_description=long_descr,
    long_description_content_type='text/markdown',
    author="Marcus Vinicius",
    author_email="viniips@hotmail.com",
    install_requires=[
        "docopt==0.6.2",
        "PyInquirer==1.0.2",
        "requests==2.20.0",
        "mechanicalSoup==0.11.0",
        "demjson==2.2.4",
        "websocket-client==0.53.0"
    ],
    url="https://github.com/vininjr/urigui",
    license='Apache 2.0'
)
