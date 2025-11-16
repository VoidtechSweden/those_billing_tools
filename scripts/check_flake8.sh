#!/bin/sh

if [ "$(uname -s)" = "Linux" ]; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi
RUN_FLAKE8="$PYTHON_CMD -m pipenv run flake8 --ignore=E501,E203,W503"
RET=0

if [ "$1" = "all" ]; then
    echo "Checking all Python files in repo"
    $RUN_FLAKE8 .
    RET=$?
else
    echo "Checking committed Python files"  
    files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')
    if [ -n "$files" ]; then
        $RUN_FLAKE8 $files
        RET=$?
    else
        echo "No Python files to check."
    fi
fi
    
exit $RET