# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END

import os
import sys
import time
from aiohttp import web
import foglamp_daemon


async def ping(request):
    """
    Heartbeat check for foglampd server running either in background or foreground

    :return: basic health information json payload. Will return uptime 0 if server is not running
    {'uptime': 32892} Time in seconds since FogLAMP started
    """

    # Since foglamp can be started in foreground or as a daemon, need to check for both foglampd and foglamp
    process_info = foglamp_daemon.find_process_info('foglampd') or foglamp_daemon.find_process_info('foglamp')

    since_started = 0
    if process_info is not None:
        since_started = time.time() - process_info['start_time']

    return web.json_response({'uptime': since_started})


async def server_start(request):
    """
    Start foglampd server

    :param request:
    :return:
    """
    retmsg = foglamp_daemon.start_server_process()
    return web.json_response({'foglamp daemon status': foglamp_daemon.is_running()})


async def server_stop(request):
    """
    Stop foglampd server

    :param request:
    :return:
    """
    retmsg = foglamp_daemon.stop()
    return web.json_response({'foglamp daemon status': foglamp_daemon.is_running()})


async def server_restart(request):
    """
    Restart foglampd server

    :param request:
    :return:
    """
    retmsg = foglamp_daemon.restart_server_process()
    return web.json_response({'foglamp daemon status': foglamp_daemon.is_running()})


async def server_status(request):
    """
    Get foglampd server status

    :param request:
    :return:
    """
    return web.json_response({'foglamp daemon status': foglamp_daemon.is_running()})


async def server_pid(request):
    """
    Get PID of foglampd server

    :param request:
    :return:
    """
    return web.json_response({'foglamp daemon pid': foglamp_daemon.get_pid()})
