wget https://github.com/alois66/Talkie_Nedap/archive/master.zip
unzip master.zip
mkdir Talkie_Nedap
cp -r -f Talkie_Nedap-master/* Talkie_Nedap/*
rm -r -f Talkie_Nedap-master
rm master.zip
sudo pip install flask
sudo pip install RPi.GPIO
sudo apt-get install mplayer
sudo apt-get install libav-tools
sudo dpkg -i pico_build/libttspico-data_1.0+git20110131-2_all.deb
sudo dpkg -i pico_build/libttspico0_1.0+git20110131-2_armhf.deb
sudo dpkg -i pico_build/libttspico-utils_1.0+git20110131-2_armhf.deb
sudo cp Talkie_Nedap/Talkie_init /etc/init.d/
sudo chown root:root /etc/init.d/Talkie_init
sudo chmod 0755 /etc/init.d/Talkie_init
sudo /etc/init.d/Talkie_init enable
sudo /etc/init.d/Talkie_init start
