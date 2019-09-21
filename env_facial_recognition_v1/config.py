from six.moves import configparser
config = configparser.ConfigParser()
config.read("parameters.ini")

def get(a,b):
    return config.get(a,b)