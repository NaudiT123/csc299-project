# Tasks4 - OpenAI Task Summarizer

A simple Python package that uses the OpenAI Chat Completions API to summarize paragraph-length task descriptions into short phrases.

## Features

- Summarizes lengthy task descriptions using GPT-4o-mini
- Processes multiple task descriptions in a single run
- Easy to run with `uv`

## Prerequisites

- Python 3.8 or higher
- `uv` package manager
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/NaudiT123/csc299-project.git 
cd csc299-project/tasks4
```

2. Install dependencies:
```bash
uv sync
```

3. Create a '.env' file:
```
OPENAI_API_KEY=your-actual-key-here
```
## Usage

Run the task summarizer:
```bash
uv run tasks4
```
or:
```bash
uv run python main.py
```

This will summarize two sample task descriptions and print the results.

## Example Output

```
Task 1: Prepare quarterly board presentation
Task 2: Organize home office space
```

## Project Structure

```
tasks4/
├── main.py              # Main application code
├── pyproject.toml       # Project configuration
├── .gitignore           # Excludes .env
├── .env.example         # Template
└── README.md            # This file
```

