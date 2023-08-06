import io
from setuptools import setup, find_packages

requirements = [
    "appdirs>=1.4.4",
    "lassie>=0.11.7",
    "readability-lxml>=0.8.1",
    "backoff>=1.10.0",
    "beautifulsoup4>=4.5.3",  # lowered because lassie is on an old dep, to work with new pip feature resolver
    "click>=7.1.2",
    "requests",
    "logzero",
]

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="url_metadata",
    version="0.1.5",
    url="https://github.com/seanbreckenridge/url_metadata",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=("""A cache which saves URL metadata and summarizes content"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=find_packages("src"),
    zip_safe=False,
    package_dir={"": "src"},
    install_requires=requirements,
    keywords="url cache metadata youtube subtitles",
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "url_metadata = url_metadata.__main__:main",
        ]
    },
    extras_require={
        "testing": [
            "pytest",
            "mypy",
            "vcrpy",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
