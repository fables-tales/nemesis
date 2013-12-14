
from ConfigParser import SafeConfigParser
import os.path

config = None

def _read_config():
    global config
    config = SafeConfigParser()

    baseDir = os.path.dirname(__file__)
    config_ini = os.path.join(baseDir, 'config.ini')
    local_ini = os.path.join(baseDir, 'local.ini')

    config.readfp(open(config_ini))
    config.read([local_ini])

if config is None:
    _read_config()
