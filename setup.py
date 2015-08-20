"""\
Provides a command line tool to fetch the citation for an academic paper
in bibtex format.

Usage:

(to search)
pyopl --search --engines=crossref "you talking to me caines"

(to fetch)
pyopl --fetch --engines=crossref 10.1515/9783110274059.177
"""

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    sys.exit("""Error: Setuptools is required for installation.
-> http://pypi.python.org/pypi/setuptools""")

setup(
    name="pyopl",
    version="0.1",
    description="Locates and fetches academic citations in bibtex format",
    author="Dimitrios Alikaniotis",
    author_email="da352@cam.ac.uk",
    url="http://github.com/dimalik/pyopl",
    packages=find_packages(),
    keywords=["arxiv", "bibtex", "latex", "citation"],
    entry_points={
        'console_scripts': ['pyopl = pyopl.__main__:main']    
    },
    license="BSD",
    install_requires=[
        'arxiv2bib',
        'feedparser'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Environment :: Console"
    ],
    long_description=__doc__,    
)
