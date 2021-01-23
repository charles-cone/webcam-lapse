# Webcam Lapse Interface
___
A Python program for time lapses using a webcam, with a web configuration page. Designed for Raspberry Pi but
should support most PC's, albeit without GPIO control.

## Usage:
___
### Docker:
Install with `docker pull charlescone:webcam-lapse-interface` and then 
`docker run -p80:8000 --privleged -d charlescone/webcam-lapse-interface`

### Standalone:
Install `fswebcam` and `pip install -r requirements.txt` then `sudo run python3 main.py`

#### Note:
If GPIO is not needed the `--privliged` and `sudo` can be omitted 

## Screenshots:
___



## Misc:
___
### Shortcomings:
- Should really be rewritten as a flask app