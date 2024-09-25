from setuptools import setup, find_packages

setup(
    name="glacier-restore-tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "kubiya_sdk",
    ],
    author="Michael Gonzalez",
    author_email="kubiyamg@gmail.com",
    description="A set of tools for managing AWS Glacier restore operations using subprocess",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/glacier-restore-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)