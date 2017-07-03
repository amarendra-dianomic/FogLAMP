# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END

from foglamp.rest_service import api


def setup(app):
    # app.router.add_route('POST', '/foglamp/a-post-req', api.a_post_req, expect_handler = aiohttp.web.Request.json)
    app.router.add_route('GET', '/foglamp/ping', api.ping)
    app.router.add_route('GET', '/foglamp/status', api.server_status)
    app.router.add_route('GET', '/foglamp/pid', api.server_pid)
    app.router.add_route('GET', '/foglamp/start', api.server_start)
    app.router.add_route('GET', '/foglamp/stop', api.server_stop)
    app.router.add_route('GET', '/foglamp/restart', api.server_restart)

    # enable cors only in dev mode ?!
    enable_cors(app)
    # a live debugger (watcher) for requests
    # this will neutralize error middleware
    enable_debugger(app)


def enable_cors(app):
    import aiohttp_cors

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)


def enable_debugger(app):
    """ provides a debug toolbar for server requests """
    import aiohttp_debugtoolbar

    # TODO must be in dev mode only
    # this will be served at API_SERVER_URL/_debugtoolbar
    aiohttp_debugtoolbar.setup(app)
