# Webcam Lapse Interface
![Build Multi-Arch](https://github.com/charles-cone/webcam-lapse/workflows/Build%20Multi-Arch/badge.svg) \
A Python program for time lapses using a webcam, with a web configuration page. Designed for Raspberry Pi but
should support most PC's, albeit without GPIO control.

## Usage:
### Docker:
Install with `docker pull charlescone:webcam-lapse-interface` and then \
`docker run -d -p 80:80 -v /data:/data --device=/dev/video0:/dev/video0 --privileged charlescone/webcam-lapse`

### Standalone:
Install `fswebcam` and then `sudo run python3 main.py`

#### Note:
If GPIO is not needed the `--privliged` and `sudo` can be omitted 

## Screenshots:
<img src="/github_images/main.png" width="281"> </img>
<img src="/github_images/config.png" width="281"> </img>


## Misc:
### About:
- I wrote this to take photos with an old security camera I was gifted.
