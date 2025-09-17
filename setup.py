from setuptools import setup, find_packages

setup(
    name="ai-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "python-dotenv",
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "devhelper=main:main",  # main.py → main()
        ],
    },
)

