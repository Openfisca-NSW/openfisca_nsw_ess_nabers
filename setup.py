# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="openfisca-nsw-rules-kids-vouchers",
    version="1.3.2",
    author="OpenFisca Team",
    author_email = 'contact@openfisca.org',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description="An OpenFisca extension that adds some variables to an already-existing tax and benefit system",
    keywords = 'benefit microsimulation social tax',
    license="http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/digitalnsw/openfisca-nsw-rules-kids-vouchers",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [
        ("share/openfisca/openfisca-nsw-rules-kids-vouchers", ["CHANGELOG.md", "LICENSE", "README.md"]),
        ],
    install_requires = [
        "OpenFisca-Country-Template >= 3.8.0,  < 4",
        ],
    extras_require = {
        "dev": [
            "autopep8 ==1.4.4",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            ]
        },
    packages=find_packages(),
    )
