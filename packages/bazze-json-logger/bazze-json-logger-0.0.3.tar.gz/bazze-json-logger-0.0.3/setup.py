import re

import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name="bazze-json-logger",
    # version=get_version(),
    author="Jason Haas",
    author_email="jason@bazze.io",
    description="Simple tool for standardizing logging to JSON.",
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['python-json-logger']
)
