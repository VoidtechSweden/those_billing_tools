#!/bin/sh

RUN_BLACK="python3 -m pipenv run black --check"
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
