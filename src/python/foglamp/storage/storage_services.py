# -*- coding: utf-8 -*-
"""FOGLAMP_PRELUDE_BEGIN
{{FOGLAMP_LICENSE_DESCRIPTION}}

See: http://foglamp.readthedocs.io/

Copyright (c) 2017 OSIsoft, LLC
License: Apache 2.0

FOGLAMP_PRELUDE_END
"""

import logging
import psycopg2
import aiopg.sa
import asyncio
import aiocoap
import sqlalchemy as sa
import time
from sqlalchemy.dialects.postgresql import JSONB
import foglamp.storage.tables

"""Storage Services as needed by Processes"""

__author__ = 'Amarendra'
__version__ = '${VERSION}'


class StatisticsServices:
    @classmethod
    async def add_metrics(self, payload):
        async with aiopg.sa.create_engine(foglamp.storage.tables.db_connection_url) as engine:
            async with engine.acquire() as conn:
                try:
                    await conn.execute(foglamp.storage.tables.t_statistics.insert().values(
                        key=payload['key'], description=payload['description'], value=payload['value'], ts=time.time()))
                except psycopg2.IntegrityError:
                    logging.getLogger('statistics').exception(
                        'Error in adding statistics key {}:\n{}'.format(payload['key'], payload))

    @classmethod
    async def aggregate_metrics(self, payload):
        pass

    @classmethod
    async def get_metrics(self, payload):
        pass

    @classmethod
    async def purge_metrics(self, payload):
        pass


class DeviceServices:
    @classmethod
    async def add_reading(self, payload):
        # Required keys in the payload
        asset = payload['asset']
        timestamp = payload['timestamp']

        # Optional keys in the payload
        readings = payload.get('sensor_values', {})
        key = payload.get('key')

        # TODO: Support for nosql databases? other sqlalchemy supported databases such as mysql, sqlite?
        async with aiopg.sa.create_engine(foglamp.storage.tables.db_connection_url) as engine:
            async with engine.acquire() as conn:
                try:
                    await conn.execute(foglamp.storage.tables.t_readings.insert().values(
                        asset_code=asset, reading=readings, read_key=key, user_ts=timestamp))
                    await StatisticsServices.add_metrics({
                        'key': 'READINGS', 'description': asset, 'value': readings})
                except psycopg2.IntegrityError:
                    logging.getLogger('coap-server').exception(
                        'Duplicate key (%s) inserting sensor values:\n%s',
                        key,
                        payload)
                    await StatisticsServices.add_metrics({
                        'key': 'DISCARDED', 'description': asset, 'value': readings})

    @classmethod
    async def get_readings(self):
        pass


    @classmethod
    async def purge_readings(self):
        pass


class ConfigurationServices:
    pass


class AdminServices:
    pass


class SendServices:
    pass


class PurgeServices:
    pass