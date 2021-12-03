import datetime
from typing import Callable
from typing import Dict

import pytest

from .interface import KrakenConfig
from .interface import TickerError
from .krakenex_adaptor import KrakenexMarketplace


class KrakenexMock:
    def __init__(self, methods: Dict[str, Callable] = None):
        if methods:
            self.methods = methods
        else:
            self.methods = {}

    def query_public(self, command: str, parameters: Dict = None) -> Dict:
        return self.methods[command](parameters)

    def query_private(self, command: str, parameters: Dict = None) -> Dict:
        return self.methods[command](parameters)


def test_get_name() -> None:
    config = KrakenConfig("mock", "mock", False, {})
    market = KrakenexMarketplace(config)
    assert market.get_name() == "Kraken"


def test_get_spot_price_success() -> None:
    def ticker(parameters: Dict) -> Dict:
        assert parameters["pair"] in ["XBTEUR", "BTCEUR", "XXBTZEUR"]
        return {
            "error": [],
            "result": {
                "XXBTZEUR": {
                    "a": ["50162.20000", "1", "1.000"],
                    "b": ["50162.10000", "2", "2.000"],
                    "c": ["50162.20000", "0.00196431"],
                    "v": ["1194.93544125", "3142.87839034"],
                    "p": ["50218.07897", "50141.26546"],
                    "t": [7355, 32353],
                    "l": ["49750.00000", "49517.80000"],
                    "h": ["50552.70000", "50657.00000"],
                    "o": "50023.50000",
                }
            },
        }

    krakenex_interface = KrakenexMock({"Ticker": ticker})

    config = KrakenConfig("mock", "mock", False, {})
    market = KrakenexMarketplace(config, krakenex_interface)
    now = datetime.datetime.now()
    price = market.get_spot_price("BTC", "EUR", now)
    assert price.timestamp == now
    assert price.coin == "BTC"
    assert price.fiat == "EUR"
    assert price.last == 50162.2


def test_get_spot_price_error() -> None:
    def ticker(parameters: Dict) -> Dict:
        return {"error": ["EQuery:Unknown asset pair"]}

    krakenex_interface = KrakenexMock({"Ticker": ticker})
    config = KrakenConfig("mock", "mock", False, {})
    market = KrakenexMarketplace(config, krakenex_interface)
    now = datetime.datetime.now()
    with pytest.raises(TickerError):
        price = market.get_spot_price("AAA", "AAA", now)


def test_balance_full() -> None:
    def balance(self) -> Dict:
        return {
            "error": [],
            "result": {
                "ZEUR": "504861.8946",
                "XXBT": "504861.8946",
            },
        }
