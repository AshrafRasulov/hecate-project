from setuptools import setup, find_packages

setup(
    name="hecate-micro",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=4.0",
        "psutil>=5.9.0",
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ],
)