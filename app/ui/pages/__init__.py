"""
UI Pages for TallySync

Author: OmniMagination
Version: 1.0.0
"""

from app.ui.pages.dashboard import DashboardPage
from app.ui.pages.ledgers import LedgersPage
from app.ui.pages.vouchers import VouchersPage
from app.ui.pages.sync_center import SyncCenterPage
from app.ui.pages.settings import SettingsPage
from app.ui.pages.logs import LogsPage

__all__ = [
    "DashboardPage",
    "LedgersPage",
    "VouchersPage",
    "SyncCenterPage",
    "SettingsPage",
    "LogsPage",
]
