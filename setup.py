from setuptools import setup, find_packages

setup(
    name="lif-qif-eif-gain-function",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "brian2",       
        "matplotlib",   
        "numpy",        
    ],
)
