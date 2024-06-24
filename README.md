[![OpenIPC logo][logo]][site_basic]

## pyosd
simple python OSD app for openipc groundstation to run on MacOS / Ubuntu

using gtk3.0 transparent window + pymavlink

work in progress

## Installation
### 1. Install dependencies
- download and install python 3.11 or 3.12 : https://www.python.org/downloads/
- python packages : PyGObject, pymavlink
```
$ pip3 install PyGObject pymavlink
```

### 2. Install gstreamer for playing video stream

This osd app could show only osd elements. so gstreamer is needed to play the video stream from air unit.

- using homebrew on MacOS
```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
$ brew install gstreamer
```

- using apt-get on Ubuntu
```
$ sudo apt-get update
$ sudo apt-get install gstreamer1.0-tools gstreamer1.0-alsa \
 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
 gstreamer1.0-libav
$ sudo apt-get install libgstreamer1.0-dev \
 libgstreamer-plugins-base1.0-dev \
 libgstreamer-plugins-good1.0-dev \
 libgstreamer-plugins-bad1.0-dev 
```

### 3. Git clone this repository and run pyosd.py

```
$ git clone https://github.com/OpenIPC/pyosd.git
$ cd pyosd
$ python3 pyosd.py 
```

## Usage
1. udp packets of video and telemetry from air unit are needed ( running wfb-ng )

   - MacOS : using utm virtual machine for installation and running wfb-ng on ubuntu-server
   - Ubuntu : install and run wfb-ng
   - wfb-ng ubuntu install guide : https://github.com/svpcom/wfb-ng?tab=readme-ov-file#quick-start-using-ubuntu-ground-station

2. playing video stream by gstreamer pipeline.
```
$ gst-launch-1.0 -vvvv udpsrc port=5600 ! application/x-rtp, payload=32, clock-rate=90000 ! queue max-size-buffers=1 \
! rtph265depay ! h265parse ! avdec_h265 ! autovideosink sync=false -e
```

3. running pyosd.py on the pyosd directory
```
$ python3 pyosd.py 
```



*** If you want to use pyosd on Ubuntu, replacing the pymavlink connection from 'udpin:224.0.0.1:14550' to 'udpin:127.0.0.1:14550'

- 173 line of pyosd.py  : https://github.com/OpenIPC/pyosd/blob/94451877e6558df44f6bf3085e632ff6120e89b1/pyosd.py#L173C9-L173C86
```
self.mavlink_connection = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
```



*** If you want to use pyosd on MacOS, mulitcating the udp packets from utm virtual machine is needed. by replacing peer of video mavlink and video 'connect://224.0.0.1:14550' of utm virtual ubuntu-server.
```
$ sudo nano /etc/wifibroadcast.cfg
...
[gs_mavlink]
peer = 'connect://224.0.0.1:14550'  # outgoing connection
# peer = 'listen://0.0.0.0:14550'   # incoming connection

[gs_video]
peer = 'connect://224.0.0.1:5600'  # outgoing connection for
                                   # video sink (QGroundControl on GS)
```


*** when starting this app on MacOS, there are some gliches. then minimizing and re-maximizing window could be helpful.


## Examples
1. MacOS (14.2.1 Sonoma)
<img width="1080" alt="MacOS" src="https://github.com/betaflight/betaflight/assets/165914105/262a60c6-80a4-43f6-a6ef-95f4fd46b926">



2. Ubuntu (23.10 mantic)
<img width="1080" alt="Ubuntu" src="https://github.com/betaflight/betaflight/assets/165914105/b8753553-562f-44be-acbd-aa8fe682ae19">

[logo]: https://openipc.org/assets/openipc-logo-black.svg
[site_basic]: https://openipc.org
