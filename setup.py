from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rc-file-analiser",
    version="0.0.1",
    author="Faycal Djilali",
    author_email="faycal.djilali6@gmail.com",
    description="A tool for analyzing and processing various file types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faycaldjilali/rcfileanaliser",
    packages=find_packages(include=['src', 'src.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'rcfileanaliser': ['*'],
        'src': ['*'],
        'src.utils': ['*'],
        'src.models': ['*'],
        'src.data': ['*'],
    },
    entry_points={
        'console_scripts': [
            'rcfileanaliser=src.app:main',
        ],
    },
)
