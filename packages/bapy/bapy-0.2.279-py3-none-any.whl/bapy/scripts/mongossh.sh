#!/usr/bin/env bash

if [[ "$(hostname)" =~ ^pro$|^book$|^gp ]]: then
    echo si
    kill -9 "$( lsof -i :9999 | grep ^ssh | awk '{print $2}' )" > /dev/null 2>&1
    ssh  -fN   -l root -L 9999:localhost:27017 67.202.15.57 > /dev/null 2>&1
fi
