from setuptools import setup, find_packages

setup(
    name="pysmshub",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
    ],
    python_requires=">=3.8",
    author="kuudori",
    description="A Python wrapper for the SmsHub API supporting synchronous and asynchronous requests.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kuudori/pysmshub",
)
