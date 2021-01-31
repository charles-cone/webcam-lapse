import Config as c
import LapseController as ci
from server import WebInterface as wi


def main():
    while True:
        lapse = c.LapseConfig()
        serv = wi.WebInterface()

        serv.run_server()

        cam = ci.LapseController()
        cam.start_lapse(lapse)


if __name__ == '__main__':
    main()
