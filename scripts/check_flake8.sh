#!/bin/sh

files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')
if [ -n "$files" ]; then
    python -m pipenv run flake8 --ignore=E501,E203,W503 $files
else
    echo "No staged Python files to lint."
fi
exit $?