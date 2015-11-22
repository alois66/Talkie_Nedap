wget https://github.com/alois66/Talkie_Nedap/archive/master.zip
unzip master.zip
mkdir Talkie_Nedap
cp -r -f Talkie_Nedap-master/* Talkie_Nedap/
rm -r -f Talkie_Nedap-master
rm master.zip
sudo apt-get update
sudo pip install flask
sudo pip install RPi.GPIO
sudo apt-get install -y mplayer
sudo apt-get install -y libav-tools
sudo dpkg -i Talkie_Nedap/pico_build/libttspico-data_1.0+git20110131-2_all.deb
sudo dpkg -i Talkie_Nedap/pico_build/libttspico0_1.0+git20110131-2_armhf.deb
sudo dpkg -i Talkie_Nedap/pico_build/libttspico-utils_1.0+git20110131-2_armhf.deb
sudo apt-get -f install
sudo mv Talkie_Nedap/Talkie /etc/init.d/
sudo chown root:root /etc/init.d/Talkie
sudo chmod a+x /etc/init.d/Talkie
sudo chmod a+x Talkie_Nedap/alerte_tty.py
sudo chmod a+x Talkie_Nedap/alerte_tty.sh
sudo update-rc.d Talkie defaults 99
sudo /etc/init.d/Talkie start

