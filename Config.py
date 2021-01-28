import json


def parse_post_data(post):
    data = {}
    pairs = post.split('&')
    for pair in pairs:
        v = pair.split('=')
        # check that all data has a value
        if v[1]:
            data[v[0]] = v[1]

    return data


class Config:
    units_to_ticks = {
        "sec": 1000,
        "min": 60000,
        "hou": 3600000
    }

    def _get_ticks(self, amt, unit):
        return int(amt) * self.units_to_ticks[unit]

    def update_data(self, p_data):
        pass


class LapseConfig(Config):
    def __init__(self):
        super().__init__()
        self.interval_ticks = 0
        self.duration_ticks = 0

    def update_data(self, p_data):
        data = parse_post_data(p_data)
        if not ('i_len' in data.keys() and 'd_len' in data.keys()):
            return "No Data"

        i_ticks = self._get_ticks(data['i_len'], data['i_units'])
        d_ticks = self._get_ticks(data['d_len'], data['d_units'])
        l_config = CaptureConfig()

        error = ""
        if i_ticks > d_ticks:
            error += "Interval can not be longer then the lapse itself\n"

        if l_config.do_power_wait and i_ticks < l_config.power_wait_ticks:
            error += "Interval can not be less then the camera power on delay\n"

        if l_config.do_shutter_wait and i_ticks < l_config.shutter_wait_ticks:
            error += "Interval can not be less then the shutter delay\n"

        if (l_config.do_power_wait and l_config.do_shutter_wait) and \
                (i_ticks < l_config.power_wait_ticks + l_config.shutter_wait_ticks):
            error += "Interval must be greater then the power wait and shutter wait combined\n"

        if not error:
            self.interval_ticks = i_ticks
            self.duration_ticks = d_ticks

        return error


class CaptureConfig(Config):
    def __init__(self):
        super().__init__()
        self.do_control_power = False
        self.power_pin = 0

        self.do_power_wait = False
        self.power_wait_ticks = 0

        self.x_res = 0
        self.y_res = 0

        self.do_control_shutter = False
        self.shutter_pin = 0

        self.do_shutter_wait = False
        self.shutter_wait_ticks = 0

        # load in existing config, if config does not exist create one
        self.load_json()

    def update_data(self, p_data):
        data = parse_post_data(p_data)
        if data:
            self.load_post_data(data)
            error = ""
            if self.do_control_power and self.power_pin not in range(0, 29):
                error += f" Power pin: {self.power_pin} is not a valid WiringPi pin\n"

            if self.do_control_shutter and self.shutter_pin not in range(0, 29):
                error += f" Shutter pin: {self.shutter_pin} is not a valid WiringPi pin\n"

            if error:
                self.load_json()  # load in old config
            else:
                self.serialize_data()  # save the new config

            return error

    def serialize_data(self):
        with open("data/camera_config.json", 'w') as f:
            f.write(json.dumps(vars(self), indent=4))

    def load_json(self):
        try:
            with open("data/camera_config.json", 'r') as f:
                data = json.loads(f.read())
            for key in data:
                setattr(self, key, data[key])

        except FileNotFoundError:
            self.serialize_data()

    def load_post_data(self, p_dict):
        post_to_attr = {
            'c_power': "do_control_power",
            'c_pin': "power_pin",

            'p_time': "do_power_wait",
            'p_ticks': "power_wait_ticks",

            'x_res': "x_res",
            'y_res': "y_res",

            'c_shutter': "do_control_shutter",
            's_pin': "shutter_pin",

            's_time': "do_power_wait",
            's_ticks': "shutter_wait_ticks"
        }

        for key in p_dict:
            val = type(getattr(self, post_to_attr[key]))(p_dict[key])
            setattr(self, post_to_attr[key], val)
