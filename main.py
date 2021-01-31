import Config as c
import LapseController as ci
from server import WebInterface as wi


def main():
    lapse = c.LapseConfig()
    serv = wi.WebInterface(lapse)
    cam = ci.LapseController()

    while True:
        serv.run_server()
        cam.start_lapse(lapse)


if __name__ == '__main__':
    main()
