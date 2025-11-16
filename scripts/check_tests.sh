#!/bin/sh

if [ "$(uname -s)" = "Linux" ]; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi
$PYTHON_CMD -m pipenv run pytest
exit $?