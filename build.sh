#!/usr/bin/env bash
./bootstrap.sh
mkdir -p /data/libpostal
./configure --datadir=/data/libpostal
make
make install