TESTS.md

Prerequisites

- Python >= 3.11 and pip
- On Linux, install xvfb to enable GUI-backed tests in headless environments
- Dependencies: install from requirements/testing/all.txt and requirements/testing/extra.txt

Setup

- Create/activate a virtual environment (recommended)
- Install dependencies:
  - pip install -r requirements/testing/all.txt -r requirements/testing/extra.txt
- Install matplotlib in editable mode:
  - pip install -e .

Run tests

- Execute the full test suite:
  - pytest -rfEsXR -n auto --pyargs matplotlib.tests
- On Linux headless environments, wrap test execution with xvfb:
  - xvfb-run -s "-screen 0 1920x1080x24" pytest -rfEsXR -n auto --pyargs matplotlib.tests

Troubleshooting

- Image comparison tests can be sensitive to fonts and rendering differences across platforms.
  - Ensure consistent font availability; DejaVu fonts are commonly used.
  - On Linux, prefer xvfb-run for GUI-related tests to avoid backend issues.
  - When investigating failures, run tests serially and increase verbosity:
    - pytest -vv -n 0 --pyargs matplotlib.tests
- If failures persist, capture the detailed diff images produced by image comparison tests and review rendering differences.
