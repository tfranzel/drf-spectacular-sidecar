import os
import re

from setuptools import setup

name = "drf-spectacular-sidecar"
package = "drf_spectacular_sidecar"
description = ""
url = "https://github.com/tfranzel/drf-spectacular-sidecar"
author = "T. Franzel"
author_email = "tfranzel@gmail.com"
license = "BSD"

with open("README.rst") as readme:
    long_description = readme.read()

with open("requirements/base.txt") as fh:
    requirements = [r for r in fh.read().split("\n") if not r.startswith("#")]


def get_version(package):
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE
    ).group(1)


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Documentation",
        "Topic :: Software Development :: Code Generators",
    ],
    project_urls={
        "Source": "https://github.com/tfranzel/drf-spectacular-sidecar",
        "Documentation": "https://drf-spectacular.readthedocs.io",
    },
)
