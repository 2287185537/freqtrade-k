"""
Stub for ExchangeWS - WebSocket functionality not needed for backtesting.
"""
import logging
from typing import Any


logger = logging.getLogger(__name__)


class ExchangeWS:
    """
    Stub class for WebSocket exchange functionality.
    Not used in backtesting-only version.
    """

    def __init__(self, config: dict, ccxt_object: Any):
        """
        Initialize WebSocket stub.
        
        :param config: Configuration dictionary
        :param ccxt_object: CCXT exchange object
        """
        self.config = config
        self.ccxt_object = ccxt_object
        logger.debug("ExchangeWS stub initialized (WebSocket not active in backtesting mode)")

    async def cleanup(self):
        """Cleanup stub - no-op."""
        pass
