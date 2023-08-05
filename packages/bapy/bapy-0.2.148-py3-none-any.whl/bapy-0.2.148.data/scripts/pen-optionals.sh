#!/usr/bin/env bash
export starting="${BASH_SOURCE[0]}"; debug.sh starting

if [[ "${VIRTUAL_ENV-}" ]]; then
  PYTHON38_PACKAGES="${VIRTUAL_ENV}/lib/python3.8/site-packages"
  PYTHON38="${VIRTUAL_ENV}/bin/python3.8"
fi

## DOMAINED
tool=domained
install="${PYTHON38_PACKAGES}/${tool}"
if [[ "${VIRTUAL_ENV-}" ]]; then
  DOMAINED_DIR="${PYTHON38_PACKAGES}/"${tool}
fi
if ! test -d "${DOMAINED_DIR}"; then
  if ${SUDO} git clone https://github.com/cakinney/domained.git "${install}"; then
    if cd "${DOMAINED_DIR}"; then
      ${SUDO} touch __init__.py
      info.sh "${tool}" downloaded "${DOMAINED_DIR}"
      if test -n "${DARWIN}"; then
        LD_LIBRARY_PATH="$(brew --prefix openssl)/lib"; export LD_LIBRARY_PATH
        CPATH="$( xcrun --show-sdk-path )/usr/include:$(brew --prefix openssl)/include"; export CPATH
        PKG_CONFIG_PATH="$(brew --prefix openssl)/lib/pkgconfig"; export PKG_CONFIG_PATH
      fi
      ${SUDO} "${PYTHON38}" -m pip install -r ./ext/requirements.txt
      if ${SUDO} "${PYTHON38}" domained.py --install; then
        info.sh "${tool}" installed "${install}"
      else
        error.sh "${tool}" install "${install}"; exit 1
      fi
    else
      error.sh "${tool}" download "${install}"; exit 1
    fi
  else
    error.sh "${tool}" download "${install}"; exit 1
  fi
fi

unset starting packages tool install
