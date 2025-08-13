# Setup

## 1 Python environment

- macOS/Linux (Python 3.9+)

Create (if missing) and/or activate the virtual environment:

```bash
# create venv (only if it does not exist)
/usr/bin/python3 -m venv "./venv"

# activate (zsh/bash)
source "./venv/bin/activate"
```

Install dependencies:

```bash
pip install -r "./requirements.txt"
```

## Configuration

Copy the example env and set your credentials:

```bash
cd "/Users/kate/future/ML-In-Era-by-Professor-HungYi-Lee/courses/ML 2025 Spring/homework/hw1"
cp env.example .env
# edit .env to set OPENAI_API_KEY and (optionally) OPENAI_MODEL
```

Required:

- `OPENAI_API_KEY`

Optional (defaults to `gpt-4o-mini` if not set):

- `OPENAI_MODEL`

## Run

```bash
python "./main.py"
```

Expected: successful client initialization. If `OPENAI_API_KEY` is missing, the program raises an error.

## Deactivate (optional)

```bash
deactivate
```

## Frequently used command

- activate the virtual env

```bash
# On macOS/Linux
source venv/bin/activate
pip freeze > requirements.txt

```

- Extract package installment list from `venv`

```bash
pip freeze > requirements.txt
```

- install the dependencies listed in `requirements.txt`

```bash
pip install -r "./requirements.txt"
```

- deactivate virtual env

```bash
deactivate
```
