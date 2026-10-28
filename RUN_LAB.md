# Running the completed lab in VS Code

Open this repository folder in VS Code. `.vscode/settings.json` points Python to the local `.venv` interpreter. If VS Code asks for an interpreter, choose `.venv/bin/python`.

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

## Files to inspect

- `electricity_bill.py`: cleaned program.
- `issues.md`: issue table, original line numbers, fixes, results and limits.
- `reflection.md`: clearly labelled reflection notes; the official questions were absent from the supplied handout.
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

The virtual environment itself is local and is not committed. Keep the `reports/before/` evidence unchanged. To regenerate final reports:

```sh
python -m pylint electricity_bill.py > reports/after/pylint_report.txt
python -m bandit -r electricity_bill.py > reports/after/bandit_report.txt
python -m flake8 electricity_bill.py > reports/after/flake8_report.txt
```

## Three fix commits

1. Bandit: safe XML parser, remove unused password, replace shell command, preserve baseline reports and environment setup.
2. Pylint: safe default, identifiers, docstrings, unused argument, UTF-8 encoding and demo import/repeat safeguards.
3. Flake8: final formatting, refreshed reports, regression tests and documentation.

The upstream class repository is unchanged. Work belongs to the personal fork `hagemaruwu/L5_30_electricity_bill` on `main`.
