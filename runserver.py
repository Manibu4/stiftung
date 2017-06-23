"""
Module to run the application.
"""

#import logging, logging.config, yaml
#logging.config.dictConfig(yaml.load(open('stiftung/settings/logging.conf')))
import logging
from stiftung.run_it import blu

blu.run(host='0.0.0.0')
