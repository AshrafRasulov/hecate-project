from setuptools import setup, find_packages

setup(
    name="hecate-core",
    version="0.1.0",
    packages=find_packages(),
    install_package_data=True,
    install_requires=[
        "pydantic>=2.0.0",  # Use Pydantic for data validation and settings management
    ],
)