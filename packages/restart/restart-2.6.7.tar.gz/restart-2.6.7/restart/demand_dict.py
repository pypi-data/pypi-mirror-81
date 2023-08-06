"""Get Demand Rates from Dictionary.

The original model based on DOH levels
"""
from typing import Optional

import confuse  # type: ignore

from .demand import Demand  # type: ignore
from .log import Log  # type: ignore
from .organization import Organization  # type: ignore
from .population import Population  # type: ignore
from .resourcemodel import Resource  # type: ignore


class DemandDict(Demand):
    """Calculate demand reading from the data dictionary.

    Overrides the Demand class and most of the calculations are there
    as the default is to use the dictionaries
    """

    def __init__(
        self,
        config: confuse.Configuration,
        res: Resource,
        pop: Optional[Population] = None,
        org: Optional[Organization] = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize Demand of Resources.

        Calculates the total, costs and per capita demand
        """
        # the init sets all variables from dictionary by default
        super().__init__(config, res, pop, log_root=log_root)
        log = self.log
        log.debug(f"In {__name__}")

        self.pop = pop
        self.res = res
        # These are the core calculations are run wth a single recalc
        self.recalc()
