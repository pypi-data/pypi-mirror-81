import setuptools

with open("README.md", "r", encoding='UTF8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="PercentRD",
    version="0.1",
    author="DevStorm",
    author_email="storm@stormdev.club",
    description="Percent Random Return",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AODevStorm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)