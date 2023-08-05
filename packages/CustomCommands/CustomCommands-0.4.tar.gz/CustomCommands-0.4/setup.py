import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CustomCommands",
    version="0.4",
    author="DevStorm",
    author_email="storm@stormdev.club",
    description="Discord Bot Custom Commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AOStormDev/Discord-Custom-Commands",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)