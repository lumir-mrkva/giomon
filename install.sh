#!/usr/bin/env bash
pip3 install -r ./requirements.txt
cp monitor.py /usr/bin
ln -s monitor.service /etc/systemd/system/monitor.service
