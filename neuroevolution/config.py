import os
from configparser import ConfigParser


def load_config(config_path):
    if not os.path.isfile(config_path):
        raise FileNotFoundError("Specified configuration file does not exist: " + os.path.abspath(config_path))

    config = ConfigParser()
    with open(config_path) as config_file:
        config.read_file(config_file)

    return config
