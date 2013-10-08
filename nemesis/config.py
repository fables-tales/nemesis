
from ConfigParser import SafeConfigParser
import os.path

config = None

def _read_config():
    global config
    config = SafeConfigParser()

    baseDir = os.path.dirname(__file__)

    config.readfp(open(os.path.join(baseDir, 'config.ini')))
    config.read([os.path.join(baseDir, 'local.ini')])

if config is None:
    _read_config()
