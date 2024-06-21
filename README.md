[![OpenIPC logo][logo]][site_basic]

## pyosd
OSD python app to run on MacOS

### Some info from Telegram chat

_> Thesedays I try to make custom osd python app to run on MacOS. Because my mavproxy osd could transparent background only in ubuntu desktop environment._

_> This is prototype of my custom osd app. I use pymavlink and gtk python lib to make transparent background window and opaque osd elements above another gstreamer video stream window._

_> I use utm virtual machine of ubuntu server 23.10 with wfb-ng, multicasting udp packets to MacOS. So far, I used asahi-ubuntu which is unable to hardware decoding, whereas it is possible on MacOS._

_> I use also betaflight fw, which has very basic osd elements. If someone make mspfwd and openipc could send telemetry with msp like mavlink in future, I could parse it with more osd elements than mavlink telemetry of betaflight._


[logo]: https://openipc.org/assets/openipc-logo-black.svg
[site_basic]: https://openipc.org
