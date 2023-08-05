#!/usr/bin/env bash

cd /tmp || exit 1
git clone https://github.com/cakinney/domained.git
cd domained || exit 1
if test -z "${DARWIN}"; then
  "${SUDO}"=sudo
fi
"${SUDO}" python3.8 domained.py --install
"${SUDO}" pip3 install -r ./ext/requirements.txt


