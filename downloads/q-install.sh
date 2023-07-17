#!/usr/bin/env bash

set -euo pipefail

if [ ! -f master.zip ]; then
    wget https://github.com/harelba/q/archive/refs/heads/master.zip
fi
unzip master.zip

pushd q-master >/dev/null
    sed -i '/package_dir=*/c\' setup.py
    sed -i '/packages=*/c\    packages=["bin"],' setup.py

    python setup.py build
    python setup.py install
popd

