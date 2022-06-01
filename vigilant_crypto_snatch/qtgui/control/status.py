import datetime
import threading
import time
from typing import Any
from typing import List
from typing import Optional

from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from vigilant_crypto_snatch.configuration import Configuration
from vigilant_crypto_snatch.datastorage import make_datastore
from vigilant_crypto_snatch.historical import CachingHistoricalSource
from vigilant_crypto_snatch.historical import CryptoCompareHistoricalSource
from vigilant_crypto_snatch.historical import DatabaseHistoricalSource
from vigilant_crypto_snatch.historical import MarketSource
from vigilant_crypto_snatch.marketplace import make_marketplace
from vigilant_crypto_snatch.paths import user_db_path
from vigilant_crypto_snatch.qtgui.ui.status import StatusTab
from vigilant_crypto_snatch.triggers import BuyTrigger
from vigilant_crypto_snatch.triggers import make_triggers
from vigilant_crypto_snatch.triggers import Trigger
from vigilant_crypto_snatch.watchloop import process_trigger


class StatusTabController:
    def __init__(self, ui: StatusTab):
        self.ui = ui
        self.wire_ui()
        self.watch_worker: Optional[WatchWorker] = None

    def wire_ui(self):
        self.ui.watch_triggers.stateChanged.connect(self.watch_triggers_changed)

        self.spot_price_model = DumbTableModel()
        self.spot_price_model.columns_names = ["Coin", "Value", "Fiat"]
        self.ui.prices.setModel(self.spot_price_model)

        self.balances_model = DumbTableModel()
        self.balances_model.columns_names = ["Asset", "Value"]
        self.ui.balance.setModel(self.balances_model)

    def config_updated(self, config: Configuration):
        self.config = config
        self.market = make_marketplace(
            config.marketplace, config.bitstamp, config.kraken, config.ccxt
        )
        datastore = make_datastore(user_db_path)

        database_source = DatabaseHistoricalSource(
            datastore, datetime.timedelta(minutes=5)
        )
        crypto_compare_source = CryptoCompareHistoricalSource(config.crypto_compare)
        market_source = MarketSource(self.market)
        caching_source = CachingHistoricalSource(
            database_source, [market_source, crypto_compare_source], datastore
        )
        self.active_triggers = make_triggers(
            config.triggers, datastore, caching_source, self.market
        )

        self.trigger_table_model = TriggerTableModel(
            [
                trigger
                for trigger in self.active_triggers
                if isinstance(trigger, BuyTrigger)
            ]
        )
        self.ui.active_triggers.setModel(self.trigger_table_model)
        self.ui.active_triggers.verticalHeader().setVisible(True)
        # self.ui.active_triggers.verticalHeader().setFixedWidth(100)

        self.active_asset_pairs = {spec.asset_pair for spec in config.triggers}

        self.toggle_worker_thread(self.ui.watch_triggers.isChecked())

    def watch_triggers_changed(self):
        self.toggle_worker_thread(self.ui.watch_triggers.isChecked())

    def toggle_worker_thread(self, desired_state: bool) -> None:
        if self.watch_worker is not None:
            self.watch_worker.running = False

        if desired_state:
            self.watch_worker = WatchWorker(
                self, self.config.polling_interval, self.active_triggers
            )
            self.watch_worker_thread = threading.Thread(target=self.watch_worker.run)
            self.watch_worker_thread.start()
        else:
            self.watch_worker = None

    def _update_balance_worker(self):
        self.balances_model.set_cells(
            [
                [coin, balance]
                for coin, balance in sorted(self.market.get_balance().items())
            ]
        )

        prices = {
            asset_pair: self.market.get_spot_price(asset_pair, datetime.datetime.now())
            for asset_pair in self.active_asset_pairs
        }
        self.spot_price_model.set_cells(
            [
                [asset_pair.coin, price.last, asset_pair.fiat]
                for asset_pair, price in sorted(prices.items())
            ]
        )

    def shutdown(self):
        if self.watch_worker is not None:
            self.watch_worker.running = False

    def ui_changed(self):
        self._update_balance_worker()
        self.trigger_table_model.endResetModel()


class WatchWorker:
    def __init__(
        self,
        status_tab_controller: StatusTabController,
        sleep: int,
        triggers: List[Trigger],
    ):
        self.running = True
        self.status_tab_controller = status_tab_controller
        self.sleep = sleep
        self.triggers = triggers

    def run(self) -> None:
        while self.running:
            for trigger in self.triggers:
                process_trigger(trigger)
            self.status_tab_controller.ui_changed()
            for i in range(self.sleep):
                time.sleep(2)
                if not self.running:
                    return


class TriggerTableModel(QAbstractTableModel):
    def __init__(self, triggers: List[BuyTrigger]):
        super().__init__()
        self.triggers = triggers
        self.keys = list(sorted(triggers[0].triggered_delegates.keys()))

    def data(self, index, role=None):
        trigger = self.triggers[index.row()]
        key = self.keys[index.column()]
        delegate = trigger.triggered_delegates[key]

        if role == Qt.ItemDataRole.DisplayRole:
            if delegate is None:
                return "—"
            if delegate.is_triggered(datetime.datetime.now()):
                return "Ready"
            else:
                return "Waiting"

        if role == Qt.ItemDataRole.DecorationRole:
            if delegate is None:
                return QColor("#afafaf")
            if delegate.is_triggered(datetime.datetime.now()):
                return QColor("#4daf4a")
            else:
                return QColor("#e41a1c")

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.triggers)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.keys)

    def headerData(self, index, orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.keys[index]

            if orientation == Qt.Orientation.Vertical:
                return self.triggers[index].get_name()


class DumbTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.columns_names: List[str] = []
        self.row_names: List[str] = []
        self.cells: List[List[Any]] = []
        self.colors: List[List[str]] = []

    def set_cells(self, cells: List[List[Any]]):
        self.beginResetModel()
        self.cells = cells
        self.endResetModel()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.cells)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.columns_names)

    def headerData(self, index, orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if self.columns_names:
                    return self.columns_names[index]
                else:
                    return ""

            if orientation == Qt.Orientation.Vertical:
                if self.row_names:
                    return self.row_names[index]
                else:
                    return ""

    def data(self, index, role=None):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.cells[index.row()][index.column()]

        if role == Qt.ItemDataRole.DecorationRole and self.colors:
            return QColor(self.colors[index.row()][index.column()])
