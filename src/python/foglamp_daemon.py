"""Runs foglamp as a daemon"""

import os

import argparse
import logging
import signal
import sys
import time
import daemon
from daemon import pidfile

from foglamp.controller import start

PIDFILE = '~/var/run/foglamp.pid'
LOGFILE = '~/var/log/foglamp.log'
WORKING_DIR = '~/var/log'

def do_something(logf):
    """
    :param logf: log file
    """
    file_handler = logging.FileHandler(logf)
    file_handler.setLevel(logging.DEBUG)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    file_handler.setFormatter(formatter)

    logger = logging.getLogger('')
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    start()


def start_daemon(pidf, logf, wdir):
    """
    Launches the daemon

    :param pidf: pidfile
    :param logf: log file
    :param wdir: working directory
    """

    # XXX: pidfile is a context
    with daemon.DaemonContext(
        working_directory=wdir,
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf)
    ) as context:
        do_something(logf)


def stop_daemon(pidf=PIDFILE):
    """
    Stop the daemon
    """

    # Get the pid from the pidfile
    pid = get_pid(pidf)

    if pid is None:
        message = "pidfile %s does not exist. Daemon not running?\n"
        sys.stderr.write(message % pidf)
        return  # not an error in a restart

    # Try killing the daemon process
    try:
        while True:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.1)
    except OSError as err:
        err = str(err)
        if err.find("No such process") > 0:
            if os.path.exists(os.path.expanduser(pidf)):
                os.remove(os.path.expanduser(pidf))
        else:
            sys.stdout.write(str(err))
            sys.exit(1)


def restart_daemon(pidf=PIDFILE):
    """
    Launches the daemon

    :param pidf: pidfile
    :param logf: log file
    :param wdir: working directory
    """

    if is_running(pidf):
        stop_daemon(pidf)
    start_daemon(pidf=os.path.expanduser(PIDFILE),
                 logf=os.path.expanduser(LOGFILE),
                 wdir=os.path.expanduser(WORKING_DIR))


def is_running(pidf=PIDFILE):
    """
    Check if the daemon is running.
    """
    return get_pid(pidf) is not None


def get_pid(pidf=PIDFILE):
    """
    Returns the PID from pidf
    """

    try:
        pf = open(os.path.expanduser(pidf),'r')
        pid = int(pf.read().strip())
        pf.close()
    except (IOError, TypeError):
        pid = None

    return pid

def safe_makedirs(directory):
    """
    :param directory: working directory
    """
    directory = os.path.expanduser(directory)
    try:
        os.makedirs(directory, 0o750)
    except Exception as e:
        if not os.path.exists(directory):
            raise e


def main():
    safe_makedirs(WORKING_DIR)
    safe_makedirs(os.path.dirname(PIDFILE))
    safe_makedirs(os.path.dirname(LOGFILE))

    if len(sys.argv) == 1:
        start_daemon(pidf=os.path.expanduser(PIDFILE),
                     logf=os.path.expanduser(LOGFILE),
                     wdir=os.path.expanduser(WORKING_DIR))
    elif len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                start_daemon(pidf=os.path.expanduser(PIDFILE),
                             logf=os.path.expanduser(LOGFILE),
                             wdir=os.path.expanduser(WORKING_DIR))
            elif 'stop' == sys.argv[1]:
                stop_daemon()
            elif 'restart' == sys.argv[1]:
                restart_daemon()
            elif 'status' == sys.argv[1]:
                print(is_running())
            elif 'info' == sys.argv[1]:
                print(get_pid())
            else:
                print("Unknown argument")
                sys.exit(2)
            sys.exit(0)
    else:
        print("usage: foglampd start|stop|restart|status|info")
        sys.exit(2)

if __name__ == "__main__":
    main()