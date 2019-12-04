#!/usr/bin/env bash
pip3 install -r ./requirements.txt
cp monitor.py /usr/bin
cp monitor.service /lib/systemd/system
ln -s /lib/systemd/system/monitor.service /etc/systemd/system/monitor.service
systemctl enable monitor
systemctl start monitor
