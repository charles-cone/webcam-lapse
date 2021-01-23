from Camera import Camera


class ServerFile():
    def get_file(self):
        pass


class CSSFile(ServerFile):
    def __init__(self, path):
        self.content_type = "text/css"
        with open(path, 'r') as f:
            self.page_data = f.read()
        self.page_data = self.page_data.encode("utf-8")

    def get_file(self):
        return self.page_data


class PreviewFile(ServerFile):
    def __init__(self, path, c_config):
        self.content_type = "image/jpg"
        self.config = c_config
        self.path = path

    def get_file(self):
        cam = Camera(self.config)
        cam.take_photo(self.config, self.path)
        with open(self.path, 'rb') as f:
            return f.read()


class ICOFile(ServerFile):
    def __init__(self, path):
        self.content_type = "image/ico"
        with open(path, 'rb') as f:
            self.page_data = f.read()

    def get_file(self):
        return self.page_data


class HTMLFile(ServerFile):
    def __init__(self, path, config):
        super().__init__()
        self.config = config
        self.content_type = "text/html"
        self.error = ""
        with open(path, 'r') as f:
            self.page_data = f.read()

    def handle_post(self, p_data):
        return bool

    def get_file(self):
        return bytes


class ConfigPage(HTMLFile):
    def _format_pin(self, is_on, pin):
        if is_on:
            return f"ON Pin:{pin}"
        else:
            return "OFF"

    def _format_time(self, is_on, ticks):
        if is_on:
            return f"ON {ticks}ms"
        else:
            return "OFF"

    def get_file(self):
        pd = self.page_data.format(
            self._format_pin(self.config.do_control_power, self.config.power_pin),
            self._format_time(self.config.do_power_wait, self.config.power_wait_ticks),
            f"{self.config.x_res}px",
            f"{self.config.y_res}px",
            self._format_pin(self.config.do_control_shutter, self.config.shutter_pin),
            self._format_time(self.config.do_shutter_wait, self.config.shutter_wait_ticks)
        )

        return pd.encode("utf-8")

    def handle_post(self, p_data):
        self.error = self.config.update_data(p_data)
        return not bool(self.error)


class LapsePage(HTMLFile):
    def __init__(self, path, config, c_func):
        super().__init__(path, config)
        self.stop_server = c_func

    def handle_post(self, p_data):
        self.error = self.config.update_data(p_data)
        if not bool(self.error):
            self.stop_server()
        else:
            return False

    def get_file(self):
        return self.page_data.encode("utf-8")


class ErrorPage(HTMLFile):
    def __init__(self, path):
        super().__init__(path, None)
        self.msg = ""
        self.redirect = ""

    def set_error(self, msg, redirect):
        self.msg = msg
        self.redirect = redirect

    def get_file(self):
        return self.page_data.format(self.msg, self.redirect).encode("utf-8")
