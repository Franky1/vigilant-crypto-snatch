import datetime
from typing import Tuple

from vigilant_crypto_snatch.core import Trade
from vigilant_crypto_snatch.core import TriggerSpec
from vigilant_crypto_snatch.datastorage import ListDatastore
from vigilant_crypto_snatch.historical import MockHistorical
from vigilant_crypto_snatch.marketplace.mock import MockMarketplace
from vigilant_crypto_snatch.triggers.concrete import BuyTrigger
from vigilant_crypto_snatch.triggers.factory import make_buy_trigger


def make_drop_trigger() -> Tuple[BuyTrigger, MockHistorical]:
    datastore = ListDatastore()
    source = MockHistorical()
    market = MockMarketplace()
    trigger_spec = TriggerSpec(
        coin="BTC",
        fiat="EUR",
        drop_percentage=120.0,
        volume_fiat=25.0,
        cooldown_minutes=10,
        delay_minutes=10,
    )
    result = make_buy_trigger(datastore, source, market, trigger_spec)
    return result, source


def test_triggered() -> None:
    drop_trigger, source = make_drop_trigger()
    # The drop is so extreme that it can never be triggered.
    assert not drop_trigger.is_triggered(datetime.datetime.now())
    assert len(drop_trigger.datastore.get_all_prices()) == 0
    assert source.calls == 2


def test_cooled_off() -> None:
    drop_trigger, source = make_drop_trigger()
    # There are no trades in the DB yet.
    assert drop_trigger.has_cooled_off(datetime.datetime.now())


def test_waiting() -> None:
    drop_trigger, source = make_drop_trigger()
    now = datetime.datetime.now()
    datastore = drop_trigger.datastore
    trade = Trade(
        timestamp=now,
        trigger_name=drop_trigger.get_name(),
        volume_coin=1.0,
        volume_fiat=1.0,
        coin="BTC",
        fiat="EUR",
    )
    datastore.add_trade(trade)
    assert not drop_trigger.has_cooled_off(now)
