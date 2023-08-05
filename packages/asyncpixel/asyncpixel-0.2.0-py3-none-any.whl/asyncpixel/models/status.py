"""Status data class."""


class Status:
    """Status data object."""

    def __init__(
        self, online: bool, gameType: str = None, _mode: str = None, _map: str = None
    ) -> None:
        """Init class.

        Args:
            online (bool): online status
            gameType ([str], optional): current game. Defaults to None.
            _mode ([str], optional): game mode. Defaults to None.
            _map ([str], optional): map. Defaults to None.
        """
        self.online = online
        self.gameType = gameType
        self.mode = _mode
        self.map = _map
