from .currency_pairs import parse_currency_pairs


def test_parse_currency_pairs_success() -> None:
    response = {
        "Response": "Success",
        "Message": "",
        "HasWarning": False,
        "Type": 100,
        "RateLimit": {},
        "Data": {
            "current": [
                {
                    "exchange": "Kraken",
                    "exchange_fsym": "NANO",
                    "exchange_tsym": "ETH",
                    "fsym": "NANO",
                    "tsym": "ETH",
                    "last_update": 1573119824.74224,
                },
                {
                    "exchange": "Kraken",
                    "exchange_fsym": "NANO",
                    "exchange_tsym": "EUR",
                    "fsym": "NANO",
                    "tsym": "EUR",
                    "last_update": 1573119825.09255,
                },
            ],
            "historical": [],
        },
    }

    pairs = parse_currency_pairs(response)
    assert pairs == [("NANO", "ETH"), ("NANO", "EUR")]
