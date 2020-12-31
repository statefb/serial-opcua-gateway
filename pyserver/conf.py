import serial
import yaml


class BaseConf():
    def __init__(self, path):
        self.path = path
        self._load_conf()

    def _load_conf(self):
        with open(self.path) as f:
            self.conf = yaml.safe_load(f)

    def get_conf(self):
        raise NotImplementedError("must be overridden.")


class SerialConf(BaseConf):
    def __init__(self, path):
        super(SerialConf, self).__init__(path)

    def _get_bytesize(self):
        values = {
            5: serial.FIVEBITS,
            6: serial.SIXBITS,
            7: serial.SEVENBITS,
            8: serial.EIGHTBITS,
        }
        return values[self.conf["databits"]]

    def _get_parity(self):
        values = {
            "None": serial.PARITY_NONE,
            "Even": serial.PARITY_EVEN,
            "Odd": serial.PARITY_ODD,
            "Mark": serial.PARITY_MARK,
            "Space": serial.PARITY_MARK,
        }
        return values[self.conf["parity"]]

    def _get_stopbits(self):
        values = {
            1: serial.STOPBITS_ONE,
            15: serial.STOPBITS_ONE_POINT_FIVE,
            2: serial.STOPBITS_TWO
        }
        return values[self.conf["stopbits"]]

    def get_conf(self):
        return dict(
            port=self.conf["name"],
            baudrate=self.conf["baud"],
            bytesize=self._get_bytesize(),
            parity=self._get_parity(),
            stopbits=self._get_stopbits(),
        )


class OpcConf(BaseConf):
    def __init__(self, path):
        super(OpcConf, self).__init__(path)

    def get_conf(self):
        return self.conf
