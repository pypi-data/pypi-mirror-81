"""Watchdog objects."""


class WatchDog:
    """Base class for watchdog."""

    def __init__(
        self,
        watchdog_lastMinute: int,
        staff_rollingDaily: int,
        watchdog_total: int,
        watchdog_rollingDaily: int,
        staff_total: int,
    ) -> None:
        """Watchdog stats.

        Args:
            watchdog_lastMinute ([int]): watchdog bans in last minute
            staff_rollingDaily ([int]): bans in the day by staff
            watchdog_total ([int]): total bans
            watchdog_rollingDaily ([int]): watchdog bans that day
            staff_total ([int]): total ever staff
        """
        self.watchdog_lastMinute = watchdog_lastMinute
        self.staff_rollingDaily = staff_rollingDaily
        self.watchdog_total = watchdog_total
        self.watchdog_rollingDaily = watchdog_rollingDaily
        self.staff_total = staff_total
