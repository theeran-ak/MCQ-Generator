from setuptools import find_packages,setup

setup(
    name="mcqgenerator",
    version="1.0",
    author="theeran",
    author_email="agatheeran27@gmil.com",
    install_requires=["openai","langchain","PYPDF2","streamlit","python-dotenv"],
    packages=find_packages() #this will find all the packages by looking for the __init__.py rather than us listing the package names
    
)