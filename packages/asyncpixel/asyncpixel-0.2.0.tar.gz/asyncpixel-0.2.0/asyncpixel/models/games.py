"""Game related objects."""

import datetime


class Game:
    """Game class."""

    def __init__(
        self,
        date: datetime.datetime,
        gameType: str,
        mode: str,
        _map: str,
        ended: datetime.datetime = None,
    ) -> None:
        """Init game class.

        Args:
            date (datetime.datetime): date
            gameType (str): gametype
            mode (str): mode
            _map (str): game
            ended (datetime.datetime, optional): ended. Defaults to None.
        """
        self.date = date
        self.gameType = gameType
        self.mode = mode
        self.map = _map
        self.ended = ended
