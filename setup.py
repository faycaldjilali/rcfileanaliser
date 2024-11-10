from setuptools import find_packages, setup

setup(
    name='rc_file_analiser',
    version='0.0.1',
    author='faycal djilali',
    author_email='djilalifaycal97@gmail.com',
    install_requires=[
        "streamlit",
        "PyPDF2==3.0.1",
        "cohere==5.11.1",
        "openpyxl==3.1.5",
        "python-dotenv==1.0.1",
        "python-docx==1.1.2",


        "reportlab"
    ],
    packages=find_packages(),
)
