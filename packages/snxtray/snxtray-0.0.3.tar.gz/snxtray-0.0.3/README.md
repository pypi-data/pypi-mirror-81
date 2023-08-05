# SNX Tray
Tray Icon for snx

## Install 
``pip install snxtray``

##### Ubuntu 18.04 LTS wx build dependencies:

``make gcc libgtk-3-dev libwebkitgtk-dev libwebkitgtk-3.0-dev libgstreamer-gl1.0-0 freeglut3 freeglut3-dev python-gst-1.0 python3-gst-1.0 libglib2.0-dev ubuntu-restricted-extras libgstreamer-plugins-base1.0-dev``

## Configuration 
#### Example config
`cat $HOME/.config/snxtray.json`
```json
{
  "server": "IP/URL",
  "cert": "path to cert",
  "keep_passwd": false,
  "elevate": "pkexec" 
}
```

