"""Main class for key data."""


class Key:
    """Main class for key data."""

    def __init__(
        self, key: str, owner: str, limit: int, queriesInPastMin: int, totalQueries: int
    ) -> None:
        """Init key object.

        Args:
            key (str): key str
            owner (str): owner uuid
            limit (int): max queries per minute
            queriesInPastMin (int): last queries per minute
            totalQueries (int): total ever quries
        """
        self.key = key
        self.owner = owner
        self.limit = limit
        self.queriesInPastMin = queriesInPastMin
        self.totalQueries = totalQueries
