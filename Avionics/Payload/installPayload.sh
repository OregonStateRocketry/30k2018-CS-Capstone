#!/bin/bash

# Ensure user has root privileges
if [[ $EUID > 0 ]]
  then echo "Please run as root"
  exit
fi

apt-get -q update && apt-get -qy install \
	python3 \
	pigpio \
	python3-pip \

pip3 install -r requirements.txt

pigpiod
