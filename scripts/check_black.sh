#!/bin/sh

if [ "$(uname -s)" = "Linux" ]; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi
RUN_BLACK="$PYTHON_CMD -m pipenv run black --check"

RET=0

if [ "$1" = "all" ]; then
    echo "Checking all Python files in repo"
    $RUN_BLACK .
    RET=$?
else
    echo "Checking committed Python files"  
    files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')
    if [ -n "$files" ]; then
        $RUN_BLACK $files
        RET=$?
    else
        echo "No Python files to check."
    fi
fi

exit $RET
