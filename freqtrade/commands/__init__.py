# flake8: noqa: F401
"""
Commands module.
Contains all start-commands, subcommands and CLI Interface creation.

Note: Be careful with file-scoped imports in these subfiles.
    as they are parsed on startup, nothing containing optional modules should be loaded.
"""

from freqtrade.commands.analyze_commands import start_analysis_entries_exits
from freqtrade.commands.arguments import Arguments
from freqtrade.commands.build_config_commands import start_new_config, start_show_config
from freqtrade.commands.data_commands import (
    start_convert_data,
    start_convert_trades,
    start_download_data,
    start_list_data,
    start_list_trades_data,
)
from freqtrade.commands.db_commands import start_convert_db
from freqtrade.commands.list_commands import (
    start_list_exchanges,
    start_list_hyperopt_loss_functions,
    start_list_markets,
    start_list_strategies,
    start_list_timeframes,
    start_show_trades,
)
from freqtrade.commands.optimize_commands import (
    start_backtesting,
    start_backtesting_show,
    start_edge,
    start_hyperopt,
    start_lookahead_analysis,
    start_recursive_analysis,
)
from freqtrade.commands.strategy_utils_commands import start_strategy_update
