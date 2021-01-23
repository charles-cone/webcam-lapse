import Config as c
import LapseController as ci
from web import WebInterface as wi


def main():
    while True:
        lapse = c.LapseConfig()
        capture = c.CaptureConfig()
        serv = wi.WebInterface(lapse, capture)

        serv.run_server()

        cam = ci.LapseController(capture)
        cam.start_lapse(lapse)


if __name__ == '__main__':
    main()
