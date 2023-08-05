import re

import setuptools


def get_version():
    with open('bazze_json_logger/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


setuptools.setup(
    name="bazze-json-logger",
    # version=get_version(),
    author="Jason Haas",
    author_email="jason@bazze.io",
    description="Simple tool for standardizing logging to JSON.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['python-json-logger']
)
