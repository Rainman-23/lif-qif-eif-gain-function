from setuptools import setup, find_packages

setup(
    name="your_package_name",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "brian2",       # for brian2 functionality and preferences
        "matplotlib",   # for plotting (matplotlib.pyplot)
        "numpy",        # for numerical operations
        "scipy",        # for functionalities like UnivariateSpline from scipy.interpolate
    ],
)
