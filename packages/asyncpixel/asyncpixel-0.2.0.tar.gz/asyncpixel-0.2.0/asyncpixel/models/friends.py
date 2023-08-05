"""Data object for player friends."""

import datetime


class Friend:
    """Friend object."""

    def __init__(
        self,
        _id: str,
        uuidSender: str,
        uuidReceiver: str,
        started: datetime.datetime,
    ) -> None:
        """Initialises object.

        Args:
            _id (str): id of friend
            uuidSender (str): sender of friend request
            uuidReceiver (str): receiver of friend request
            started (datetime.datetime): start of friendship
        """
        self._id = _id
        self.uuidSender = uuidSender
        self.uuidReceiver = uuidReceiver
        self.started = started
