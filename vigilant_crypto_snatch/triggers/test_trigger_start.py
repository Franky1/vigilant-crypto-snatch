import datetime

import pytest

from vigilant_crypto_snatch.core import TriggerSpec
from vigilant_crypto_snatch.datastorage import ListDatastore
from vigilant_crypto_snatch.historical import MockHistorical
from vigilant_crypto_snatch.marketplace.mock import MockMarketplace
from vigilant_crypto_snatch.triggers.concrete import BuyTrigger
from vigilant_crypto_snatch.triggers.factory import make_buy_trigger


@pytest.fixture
def drop_trigger_with_start() -> BuyTrigger:
    datastore = ListDatastore()
    source = MockHistorical()
    market = MockMarketplace()
    trigger_spec = TriggerSpec(
        coin="BTC",
        fiat="EUR",
        volume_fiat=10.0,
        cooldown_minutes=10,
        delay_minutes=10,
        start=datetime.datetime(2021, 7, 16),
    )
    result = make_buy_trigger(datastore, source, market, trigger_spec)
    return result


def test_trigger_with_start(drop_trigger_with_start: BuyTrigger) -> None:
    before = datetime.datetime(2021, 7, 15)
    after = datetime.datetime(2021, 7, 17)
    assert not drop_trigger_with_start.has_cooled_off(before)
    assert drop_trigger_with_start.has_cooled_off(after)
