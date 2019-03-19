#!/usr/bin/env python

"""
    Configuration Manager
"""

import os
import sys
import pprint
import subprocess
import traceback
import base64
import json
import click
import datetime
import ConfigParser
from ConfigParser import SafeConfigParser


###############################################################################

def _log(msg_str, color='green', onemore=0, blink=False):
    stack = traceback.extract_stack()

    # self is '-1'
    (filename1, line1, procname1, text1) = stack[-1]

    # caller is '-2'
    (filename2, line2, procname2, text2) = stack[-2]

    if onemore:
        (filename2, line2, procname2, text2) = stack[-3]

    curdate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    click.secho('[{}] [{}] {}'.format(curdate, procname2, msg_str), fg=color, blink=blink)

###############################################################################

def _log_fatal(msg_str):
    _log(msg_str, color='red', onemore=1, blink=True)
    sys.exit(1)

###############################################################################

def _log_error(msg_str):
    _log(msg_str, color='red', onemore=1)

###############################################################################

def _log_warn(msg_str):
    _log(msg_str, color='yellow', onemore=1)

###############################################################################

def _log_info(msg_str):
    _log(msg_str, color='cyan', onemore=1)

###############################################################################

def _log_debug(msg_str):
    _log(msg_str, color='white', onemore=1)

###############################################################################
def _exec_local_cmd (_cmd):
    _log_info("[" + _cmd + "]")
    retcode = 0
    output = ''

    try:
        output = subprocess.check_output(_cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        retcode = e.returncode
        output = e.output
        pass

    return retcode, output

###############################################################################

def _json_exec(_cmd):
    d = {}

    retcode, output = _exec_local_cmd(_cmd)
    #print "retcode of cmd: ", retcode
    #print '[' + output + ']'
    try:
        d = json.loads (output)
    except Exception as e:
        return 1, str(output)

    return retcode, d

###############################################################################

def _do_package(section, function):
    name = parser.get(section, 'name')[1:-1]
    _log_debug("package name [" + name + "]")

    cmd = 'sshpass -e ssh root@{0} "/opt/config_manager/bin/{1}.bash {2} {3}"'.format(server, module, function, name)
    _log_debug(cmd)


###############################################################################

def _do_file(section, function):
    name = parser.get(section, 'destination')[1:-1]

    cmd = ""
    directory = "0"

    if function in ['create']:
        try:
            directory = parser.get(section, 'directory')[1:-1]
        except ConfigParser.NoOptionError:
            pass

        owner = parser.get(section, 'owner')[1:-1]
        mode = parser.get(section, 'mode')[1:-1]
    
        content = parser.get(section, 'content')[1:-1]
        encoded = base64.b64encode(content)

        cmd = 'sshpass -e ssh root@{0} "/opt/config_manager/bin/{1}.bash {2} {3} {4} {5} {6} {7}"'.format(server, module, function, name, directory, owner, mode, encoded)

    elif function in ['rename']:
        source = parser.get(section, 'source')[1:-1]
        cmd = 'sshpass -e ssh root@{0} "/opt/config_manager/bin/{1}.bash {2} {3} {4}"'.format(server, module, function, source, name)


    _log_debug(cmd)

    return 0


###############################################################################

server = sys.argv[1]
_log_info("server [" + server + "]")
# read spec.txt, get a list of conf files to "play" on the specified server

# evaluate config directory relative to "self" or using env variable
script_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.realpath(os.path.join(script_dir, '..', 'config'))
if os.getenv('CONFIG_DIR'):
    config_dir = os.path.realpath(os.getenv('CONFIG_DIR'))

spec_file = os.path.join(config_dir, "spec.txt")
configs = []

with open(spec_file) as fp:
    while 1:
        line = fp.readline()

        if not line:
            break

        # TODO: verify that file exists, etc.

        configs.append(line.strip())


for config in configs:
    parser = SafeConfigParser()
    cfg = os.path.join(config_dir, config)
    print "config file [" + cfg + "]"
    
    if not parser.read(cfg):
        _log_error("unable to read file (" + cfg + ")")
        continue

    for section in parser.sections():
        action = parser.get(section, 'action')[1:-1]
        module, function = action.split('.')

        if module == 'package':
            _do_package(section, function)
        elif module == 'file':
            _do_file(section, function)


        # interpret the conf file to "actionable" script execution on the remote server



