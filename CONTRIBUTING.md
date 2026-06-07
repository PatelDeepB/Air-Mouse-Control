# Contributing to AirMouse++

First off, thank you for considering contributing to AirMouse++! It's people like you that make open source tools great.

## How Can I Contribute?

### 1. Reporting Bugs
- Ensure the bug was not already reported by searching on GitHub under Issues.
- If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### 2. Suggesting Enhancements
- Open a new issue with the label `enhancement`.
- Provide a clear, detailed explanation of the feature and why it would be beneficial.

### 3. Pull Requests
- Fork the repo and create your branch from `main`.
- If you've added code that should be tested, add tests.
- Ensure the test suite passes (`pytest tests/`).
- Issue that pull request!

## Code Style Guide
We follow strict, clean, standard Python formatting:
- Use **Type Hints** on all function signatures.
- Max 300 lines per file (modules).
- Every public function/class needs a docstring.
- Add unit tests for business logic in the `tests/` folder.

## Environment Setup
To set up a dev environment, clone the repo and run:
```bash
pip install -e .[dev]
```
This will install `pytest` and `ruff` for linting and testing.
