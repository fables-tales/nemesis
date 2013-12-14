
from ConfigParser import SafeConfigParser
import logging
import logging.config
import os.path

config = None

_logging_configured = False

def _read_config():
    global config
    config = SafeConfigParser()

    baseDir = os.path.dirname(__file__)
    config_ini = os.path.join(baseDir, 'config.ini')
    local_ini = os.path.join(baseDir, 'local.ini')

    config.readfp(open(config_ini))
    config.read([local_ini])

def configure_logging():
    global _logging_configured
    if _logging_configured:
        return

    base_dir = os.path.dirname(__file__)
    logging_ini = config.get('logging', 'config_file')
    logging_ini = os.path.join(base_dir, logging_ini)

    logging.config.fileConfig(logging_ini)

    logging.info("logging configured using '{0}'.".format(logging_ini))

    _logging_configured = True

if config is None:
    _read_config()
