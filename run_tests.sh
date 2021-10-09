echo Installing dependancies...
pip install -e .
echo Running unit tests
coverage run -m unittest discover -s ./test -p test_*.py &&
coverage report --fail-under=95 --skip-empty -m --include src/* &&
flake8 --doctests src/
