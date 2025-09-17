from setuptools import setup, find_packages

setup(
    name="devhelper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "google-generativeai",
        "pyperclip"
    ],
)
