#!/bin/bash

# Initialize script path
MLC_TMP_CURRENT_SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Initialize MLC_PYTHON_BIN_WITH_PATH
MLC_PYTHON_BIN_WITH_PATH=${MLC_PYTHON_BIN_WITH_PATH:-python3}

# Run script
echo "Python path: $MLC_PYTHON_BIN_WITH_PATH"
echo "Script path: $MLC_TMP_CURRENT_SCRIPT_PATH/process.py"
${MLC_PYTHON_BIN_WITH_PATH} ${MLC_TMP_CURRENT_SCRIPT_PATH}/process.py
test $? -eq 0 || exit 1