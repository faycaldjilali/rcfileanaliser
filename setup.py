from setuptools import find_packages, setup

setup(
    name='rc_file_analiser',
    version='0.0.1',
    author='faycal djilali',
    author_email='djilalifaycal97@gmail.com',
    install_requires=[
        "cohere",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages(),
)
