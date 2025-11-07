#!/bin/sh

files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')
if [ -n "$files" ]; then
    python -m pipenv run black --check $files
else
    echo "No staged Python files to check."
fi
exit $?