#!/usr/bin/env python
#(c)2020, Anton Karneliuk


# Modules
import sys
import logging
import json
import os


# Own modules
from arg_parser import NFData
from client import gNMIclient
from artefacts.messages import msg


# Variables
path_msg = 'artefacts/messages.json'
path_log = 'log/execution.log'


# Body
if __name__ == "__main__":
    # Setting logger
    if not os.path.exists(path_log.split('/')[0]):
        os.mkdir(path_log.split('/')[0])

    logging.basicConfig(filename=path_log, level=logging.INFO, format='%(asctime)s.%(msecs)03d+01:00,%(levelname)s,%(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
    logging.info('Starting application...')

    # Collecting inputs
    del sys.argv[0]
    DD = NFData(sys.argv, msg)

    # gNMI operation
#    try:
    with gNMIclient(DD.targets, username=DD.username, password=DD.password, 
                    to_print=DD.to_print, insecure=DD.insecure, path_cert=DD.certificate) as GC:
        if DD.operation == 'capabilities':
            result = GC.capabilities()

        elif DD.operation == 'get':
            result = GC.get(DD.gnmi_path)
#    except:
#        logging.critical(f'The connectivity towards {DD.targets} cannot be established. The execution is terminated.')
#        sys.exit(1)


