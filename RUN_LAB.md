# Lab setup and commands

I used a local `.venv` for this lab. The VS Code interpreter setting is `.venv/bin/python`.

In the VS Code terminal:

```sh
source .venv/bin/activate
python electricity_bill.py
python -m pylint electricity_bill.py
python -m bandit -r electricity_bill.py
python -m flake8 electricity_bill.py
python -m unittest discover -s tests -v
git log --oneline -4
```

Flake8 prints nothing when it succeeds. The final program produces four bills and writes `bills.json` in the current directory. Run it from the repository root.

## Project files

- `electricity_bill.py`: cleaned program.
- `issues.md`: issue table, original line numbers, fixes, results and limits.
- `reflection.md`: four reflection questions and answers based on the lab.
- `reports/before/`: original reports, demo console output and JSON.
- `reports/after/`: final reports, demo output, JSON, and test results.
- `requirements.txt`: exact installed package versions, including defusedxml.
- `tests/test_electricity_bill.py`: behavioral and security regression tests.

## Re-create the environment elsewhere

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The virtual environment itself is local and is not committed. The original reports are in `reports/before/`. Commands for the final reports:

```sh
python -m pylint electricity_bill.py > reports/after/pylint_report.txt
python -m bandit -r electricity_bill.py > reports/after/bandit_report.txt
python -m flake8 electricity_bill.py > reports/after/flake8_report.txt
```

## Three fix commits

1. Bandit: safe XML parser, remove unused password, replace shell command, preserve baseline reports and environment setup.
2. Pylint: safe default, identifiers, docstrings, unused argument, UTF-8 encoding and demo import/repeat safeguards.
3. Flake8: final formatting, refreshed reports, regression tests and documentation.

My changes are on `main` in my fork, `hagemaruwu/L5_30_electricity_bill`. The class repository is unchanged.
