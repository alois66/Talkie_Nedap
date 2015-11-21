#!/bin/bash

while :
do

cd /home/pi/Talkie_Nedap
sudo python alerte_tts.py >/dev/null &
wait

done
