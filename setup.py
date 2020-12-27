import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylgb_mimec", # Replace with your own username
    version="3.0",
    author="lefufu",
    author_email="author@example.com",
    description="A python library to automatize some painfull processes in IL2 GB mission creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lefufu/PylGBMiMec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)