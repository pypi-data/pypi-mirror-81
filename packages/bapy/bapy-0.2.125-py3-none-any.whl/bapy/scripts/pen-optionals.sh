#!/usr/bin/env bash
export starting="${BASH_SOURCE[0]}"; debug.sh starting

cd /tmp || exit 1
git clone https://github.com/cakinney/domained.git
cd domained || exit 1

unset VIRTUAL_ENV PYTHONHOME
deactivate > /dev/null 2>&1

"${SUDO}" "${PYTHON38}" domained.py --install
"${SUDO}" "${PYTHON38}" -m pip install -r ./ext/requirements.txt

unset starting

