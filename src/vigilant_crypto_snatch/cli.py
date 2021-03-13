#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import logging

import coloredlogs
import yaml

from . import marketplace_factory
from . import datamodel
from . import drop
from . import telegram


logger = logging.getLogger('vigilant_crypto_snatch')


def main():
    options = _parse_args()
    config = load_config()

    if 'telegram' in config:
        telegram_handler = telegram.TelegramBot(config['telegram']['token'])
        logger.addHandler(telegram_handler)

    coloredlogs.install(level=options.loglevel.upper())

    logger.info('Starting up …')

    session = datamodel.open_db_session()
    market = marketplace_factory.make_marketplace(options.marketplace, config)

    drop.check_for_drops(config, session, market)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--greeting', action='store_true',
                        help='Show an unnecessary long greeting message during startup.')
    parser.add_argument('--marketplace', choices=['bitstamp', 'kraken', 'kraken-cli'], default='kraken')
    parser.add_argument('--restart', action='store_true',
                        help='Ignore errors and continue running. This is a bit dangerous.')
    parser.add_argument('--loglevel', choices=['debug', 'info', 'warning', 'error', 'critical'], default='info')
    options = parser.parse_args()

    return options


def load_config() -> dict:
    config_path = os.path.expanduser('~/.config/vigilant-crypto-snatch.yml')
    if not os.path.isfile(config_path):
        print(f"Please create the configuration file at {config_path}.")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config


if __name__ == '__main__':
    main()
