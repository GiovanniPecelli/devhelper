# DevHelper - Python AI Agent

DevHelper is an AI agent that helps you read, modify, and analyze project files directly from the terminal or as a Python library.

## Install DevHelper from Git
To use DevHelper in another project, install it directly from the Git repository:

```bash
- pip install git+https://github.com/GiovanniPecelli/devhelper.git

- pip install -r requirements.txt

## Import devhelper in your project

from agent_core import Agent, list_project_files, read_file, copy_file_to_clipboard

# Initialize the agent
agent = Agent("DevHelper")

# Example usage
print(agent.ask("Analyze my checkout code"))

# Main functions available:
# - list_project_files() – lists all files in the project
# - read_file(file_path) – reads a file
# - copy_file_to_clipboard(file_path) – copies a file's content to the clipboard
# - agent.modify_file(file_path, instruction) – modifies a file based on instructions using AI

# Run DevHelper as CLI

You can run DevHelper interactively from the terminal:

- python devhelper.py

# Set your Google API key in .env:

GOOGLE_API_KEY=your_api_key_here