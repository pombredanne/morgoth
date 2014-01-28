
from morgoth.config import Config
from morgoth.plugin_loader import PluginLoader
import os

import logging

logger = logging.getLogger(__name__)

_DETECTORS = {}

def register_detector(name, d_class):
    """
    Register an Detector by a given name

    @param name: the name to identify the Detector
    @param d_class: the class of the Detector
    """
    if name in _DETECTORS:
        raise ValueError('Detector of name "%s" already exists' % name)
    _DETECTORS[name] = d_class

def get_detector(name):
    """
    Return the Detector class by a given name

    @return Detector class
    """
    if name not in _DETECTORS:
        raise ValueError("Detector of name '%s' doesn't exist" % name)
    return _DETECTORS[name]


def load_detectors():
    """ Load the configured Detectors """
    from morgoth.detectors.detector import Detector
    from morgoth.detectors.scheduled import Scheduled
    dirs = [os.path.dirname(__file__)]
    dirs.extend(Config.get(['detectors', 'plugin_dirs'], []))

    pl = PluginLoader()
    mods = pl.find_modules(dirs)

    classes = pl.find_subclasses(mods, Detector, ignored=set([Scheduled.__name__]))

    for d_name, d_class in classes:
        logger.debug("Found Detector %s", d_name)
        try:
            register_detector(d_name, d_class)
        except ValueError as e:
            logger.warning("Found duplicate Detectors with name %s", d_name)

