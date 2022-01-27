import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="common_foundation",
    version="0.0.1",
    author="tomasdrah",
    author_email="tomasdrah@seznam.cz",
    description="Common structures for project fundamental functionalities",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/tomasdrah/common_foundation",
    project_urls={
        "Bug Tracker": "https://github.com/tomasdrah/common_foundation/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['common_foundation'],
    # install_requires=['requests'],
    python_requires = ">=3.10",
    )
