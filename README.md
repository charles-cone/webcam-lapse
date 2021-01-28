# Webcam Lapse Interface
A Python program for time lapses using a webcam, with a web configuration page. Designed for Raspberry Pi but
should support most PC's, albeit without GPIO control.

## Usage:
### Docker:
Install with `docker pull charlescone:webcam-lapse-interface` and then 
`docker run -p80:8000 --privleged -d charlescone/webcam-lapse-interface`

### Standalone:
Install `fswebcam` and `pip install -r requirements.txt` then `sudo run python3 main.py`

#### Note:
If GPIO is not needed the `--privliged` and `sudo` can be omitted 

## Screenshots:
<img src="/github_images/main.png" width="281"> </img>
<img src="/github_images/config.png" width="281"> </img>


## Misc:
### About:
- I wrote this to take photos with an old security camera I was gifted.
### Shortcomings:
- Should really have been written as a flask app ¯\\\_(ツ)\_/¯