from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-devhelper",  # Nome univoco per PyPI
    version="0.1.0",
    author="Il tuo nome",
    author_email="tua@email.com",
    description="Un assistente AI per sviluppatori con Google Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuousername/devhelper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "python-dotenv>=0.19.0",
        "pyperclip>=1.8.0",
        "click>=8.0.0",  # Per i comandi CLI
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.812",
        ],
    },
    entry_points={
        "console_scripts": [
            # Comando principale per interfaccia interattiva
            "devhelper=ai_agent.devhelper:main",
            # Comando per CLI (opzionale, se vuoi entrambi)
            "devhelper-cli=ai_agent.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

