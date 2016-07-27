# Setting up Linux
1. Start off with a freshly flashed image (tested on CHIP OS 4.3)
2. Open a terminal session to your CHIP (over UART)
3. Connect to internet using `sudo nmtui`
4. Update the system time with `sudo sntp -s pool.ntp.org` or `sudo sntp -s time.nist.gov` so that you can use git

# Python setup
Get some stuff
1. `sudo apt update`
2. `sudo apt install python-dev python-pip python-smbus i2c-tools build-essential git`

## Adafruit LED library
1. `git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack.git`
2. `cd Adafruit_Python_LED_Backpack`
3. `sudo python setup.py install`

## Adafruit Motor Controller library
1. `git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git`
2. `cd Adafruit_Python_PCA9685`
3. `sudo python setup.py install`

## WebSocket python server
1. `sudo pip install autobahn trollius`
3. Refer to autobahn documentation for setting up a basic server
4. Be sure to set the server up on address 10.0.0.1 with port 8080

# Wi-Fi AP setup
1. `sudo apt install hostapd dnsmasq`
2. `sudo nano /etc/hostapd.conf` and add:
  ```
  interface=wlan1
  ssid=hexacat
  driver=nl80211
  channel=1
  hw_mode=g
  ```

3. `sudo nano /etc/init.d/hostapd` and change:
  ```
  DAEMON_CONF=/etc/hostapd.conf
  ```

4. `sudo nano /etc/dnsmasq.conf` and add:
  ```
  interface=wlan1
  except-interface=wlan0
  dhcp-range=10.0.0.10,10.0.0.250,12h
  ```

5. `sudo nano /etc/network/interfaces` and add:
  ```
  source-directory /etc/network/interfaces.d

  auto wlan1
  iface wlan1 inet static
  address 10.0.0.1
  netmask 255.255.255.0
  ```

6. Enter the following and restart:
```
sudo update-rc.d hostapd enable
sudo update-rc.d dnsmasq enable
```

# Setup root auto-login
1. `sudo nano /lib/systemd/system/getty@.service` and change:<br>
  `ExecStart=-/sbin/agetty --noclear %I $TERM`<br>
  to<br>
  `ExecStart=-/sbin/agetty/ --noclear -a root %I $TERM`
2. `sudo reboot`


# Get hexacat software set up and auto start
1. Sign into root account
2. `git clone https://github.com/ianholst/hexacat`
3. `cd hexacat`
4. `chmod +x hexacat.sh`
5. `cd ..`
2. `nano .profile`
3. Add contents:
  ```
source /root/hexacat/hexacat.sh
  ```
4. `reboot`

# Hardware
main chamber: 65mm x 80mm x 55mm<br>
servo: width 11.7mm height 16 mm

# App capabilities
- Connect via websockets
- control speed and direction
- shut down machine
- Check battery
- preprogrammed tricks
- virtual console

# Servo adjustments
90 degrees clockwise on right, 45 degrees clockwise on left (facing the leg side) on right reverse (subtract from 180?) the angle going to
