#!/bin/bash
nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2