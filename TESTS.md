Matplotlib tests: headless (Linux) quick guide

Overview
- This document outlines how to run Matplotlib's test suite on a headless Linux system and troubleshoot image-comparison failures.
- It complements the developer docs in doc/devel/testing.rst.

Prerequisites
- Linux with Python 3. Install test dependencies:
  - pip install -r requirements/testing/all.txt
- A virtual X server (for GUI/image tests):
  - Debian/Ubuntu: apt-get update && apt-get install -y xvfb xauth
  - Fonts commonly needed by tests:
    - apt-get install -y fonts-dejavu-core fonts-dejavu-extra fonts-noto-core fonts-noto-cjk fonts-wqy-zenhei
  - Optional for some converters/renderers: ghostscript (gsfonts), inkscape (if testing SVG conversions)

Running tests headlessly
- Preferred: use pytest-xvfb plugin (included in requirements/testing/all.txt):
  - Command: pytest --xvfb -q
  - Add -n auto if pytest-xdist is installed to parallelize: pytest --xvfb -n auto
- Alternative: wrap pytest with xvfb-run:
  - Command: xvfb-run -a pytest -q
- Ensure a non-interactive backend is used during tests:
  - Set MPLBACKEND=Agg or rely on the test configuration to select Agg.
- Helpful environment variables for CI/headless runs:
  - NO_AT_BRIDGE=1 to disable AT-SPI (avoids dbus warnings and speed issues with some GUI toolkits).
  - QT_QPA_PLATFORM=offscreen for Qt-based backends if needed.
  - MPLCONFIGDIR set to a temporary directory to isolate local config.

Examples
- Minimal run (plugin):
  - NO_AT_BRIDGE=1 MPLBACKEND=Agg pytest --xvfb -q
- Minimal run (wrapper):
  - NO_AT_BRIDGE=1 MPLBACKEND=Agg xvfb-run -a pytest -q
- Parallel run:
  - NO_AT_BRIDGE=1 MPLBACKEND=Agg pytest --xvfb -n auto -q

Image comparison tests and troubleshooting
- Matplotlib includes many image-comparison tests using baseline_images and result_images directories.
- On failure, pytest writes artifacts under result_images/ with files such as:
  - <testname>-expected.png, <testname>-actual.png, <testname>-failed-diff.png
- Common causes of diffs:
  - Missing fonts or different font versions (check with fc-list).
  - Different FreeType or libpng versions affecting rendering.
  - Locale differences (e.g., decimal/thousands separators).
  - DPI scaling or environment-specific settings.
  - Non-determinism due to random data in a test (should be minimized by fixtures).
- Steps to resolve:
  - Verify fonts are present; install fonts-dejavu-core, fonts-noto-core, fonts-noto-cjk, fonts-wqy-zenhei.
  - Use MPLBACKEND=Agg and headless display via --xvfb or xvfb-run.
  - Clear previous artifacts: rm -rf result_images/ before re-running.
  - Inspect diffs with the helper script tools/triage_tests.py:
    - python tools/triage_tests.py result_images
  - Ensure consistent environment (MPLCONFIGDIR, locale, versions).
  - If authoring new tests, consider image_comparison tolerances (tol) and remove_text to reduce font sensitivity.

Notes
- For detailed guidance on the testing infrastructure and decorators (image_comparison, check_figures_equal), see doc/devel/testing.rst and doc/api/testing_api.rst.
- If GUI toolkit tests fail under headless environments, set NO_AT_BRIDGE=1 and ensure the toolkit selects an offscreen platform. Use Agg for non-interactive rendering where possible.

References
- pytest-xvfb: https://pypi.org/project/pytest-xvfb/
- Matplotlib testing docs (local): doc/devel/testing.rst
