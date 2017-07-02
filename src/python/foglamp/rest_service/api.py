# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END

import os
import sys
import time
from aiohttp import web
from foglamp_daemon import find_process_info, is_running, get_pid, stop_daemon, PIDFILE, LOGFILE, WORKING_DIR, start_server_process, restart_server_process

async def ping(request):
    """
    :return: basic health information json payload
    {'uptime': 32892} Time in seconds since FogLAMP started
    """

    # Since foglamp can be started in foreground or as a daemon, need to check for both foglampd and foglamp
    process_info = find_process_info('foglampd') or find_process_info('foglamp')

    since_started = 0
    if process_info is not None:
        since_started = time.time() - process_info['start_time']

    return web.json_response({'uptime': since_started})

async def server_start(request):
    retmsg = start_server_process()
    return web.json_response({'foglamp daemon status': is_running()})

async def server_stop(request):
    retmsg = stop_daemon()
    return web.json_response({'foglamp daemon status': is_running()})

async def server_restart(request):
    retmsg = restart_server_process()
    return web.json_response({'foglamp daemon status': is_running()})

async def server_status(request):
    return web.json_response({'foglamp daemon status': is_running()})

async def server_pid(request):
    return web.json_response({'foglamp daemon pid': get_pid()})
