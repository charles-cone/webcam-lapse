import time
import os


class Camera():
    __camera_controller = None
    __config = None
    __has_GPIO = False

    def __init__(self, c_config):
        Camera.__config = c_config
        Camera.__camera_controller = self._controller_factory()(c_config)

    def _controller_factory(self):
        del Camera.__camera_controller

        try:
            import RPi.GPIO as GPIO
            Camera.__has_GPIO = True
            GPIO.setmode(GPIO.BOARD)
        except ModuleNotFoundError:
            Camera.__has_GPIO = False

        config = Camera.__config
        has_gpio = Camera.__has_GPIO

        class CameraController():
            def __init__(self, c_config):
                self.x_res = c_config.x_res
                self.y_res = c_config.y_res

            def take_photo(self, path):
                start = time.time()
                os.system(f"fswebcam --no-banner -r {self.x_res}x{self.y_res} {path}")
                return time.time() - start

        if config.do_control_power and has_gpio:
            class RelayController(CameraController):
                def __init__(self, c_config):
                    self.power_pin = c_config.power_pin
                    self.do_delay = c_config.do_power_wait
                    self.delay_secs = c_config.power_wait_ticks / 1000  # ticks to secs

                    GPIO.setup(self.power_pin, GPIO.OUT)
                    super().__init__(c_config)

                def __del__(self):
                    GPIO.cleanup()

                def take_photo(self, path):
                    GPIO.output(self.power_pin, GPIO.HIGH)
                    if self.do_delay:
                        time.sleep(self.delay_secs / 1000)

                    photo_time = super(RelayController, self).take_photo(path)
                    GPIO.output(self.power_pin, GPIO.OUT)
                    return photo_time + self.delay_secs

            return RelayController

        elif config.do_control_shutter and has_gpio:
            class ExternalController(CameraController):
                def __init__(self, c_config):
                    self.power_pin = c_config.power_pin
                    self.do_power_delay = c_config.do_power_wait
                    self.power_delay_secs = c_config.power_wait_ticks / 1000  # ticks to secs

                    self.shutter_pin = c_config.shutter_pin
                    self.do_shutter_delay = c_config.do_shutter_wait
                    self.shutter_delay_secs = c_config.shutter_wait_ticks / 1000

                    super().__init__(c_config)

                def __del__(self):
                    GPIO.cleanup()

                def take_photo(self, path):
                    GPIO.output(self.power_pin, GPIO.HIGH)
                    if self.do_power_delay:
                        time.sleep(self.power_delay_secs)

                    GPIO.output(self.shutter_pin, GPIO.HIGH)
                    if self.do_shutter_delay:
                        time.sleep(self.shutter_delay_secs)

                    GPIO.output(self.shutter_pin, GPIO.LOW)
                    GPIO.output(self.power_pin, GPIO.LOW)

            return ExternalController
        else:
            return CameraController

    def take_photo(self, c_config, path):
        # check if config is changed, and adjust camera interface object accordingly
        if Camera.__config != c_config:
            Camera.__config = c_config
            self._controller_factory()

        return Camera.__camera_controller.take_photo(path)
