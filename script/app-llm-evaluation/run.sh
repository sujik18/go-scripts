#!/bin/bash

# Initialize script path
MLC_TMP_CURRENT_SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Python binary (provided by MLCFlow environment)
MLC_PYTHON_BIN_WITH_PATH=${MLC_PYTHON_BIN_WITH_PATH:-python3}

# Load environment variables from .env file
if [[ -f "${MLC_TMP_CURRENT_SCRIPT_PATH}/.env" ]]; then
  echo "Loading environment variables from ${MLC_TMP_CURRENT_SCRIPT_PATH}/.env"
  export $(grep -v '^#' "${MLC_TMP_CURRENT_SCRIPT_PATH}/.env" | xargs)
else
  echo "No .env file found in ${MLC_TMP_CURRENT_SCRIPT_PATH}. Skipping environment variable loading."
fi

# Run script
echo "Python path: $MLC_PYTHON_BIN_WITH_PATH"
echo "Script path: $MLC_TMP_CURRENT_SCRIPT_PATH/process.py"
${MLC_PYTHON_BIN_WITH_PATH} ${MLC_TMP_CURRENT_SCRIPT_PATH}/process.py
test $? -eq 0 || exit 1

