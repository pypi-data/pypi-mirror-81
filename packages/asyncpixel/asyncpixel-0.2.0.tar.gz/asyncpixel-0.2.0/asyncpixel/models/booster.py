"""Data objects for boosters."""

import datetime
from typing import List


class Booster:
    """Main booster class."""

    def __init__(
        self,
        _id: str,
        purchaserUuid: str,
        amount: int,
        originalLength: int,
        length: int,
        gameType: int,
        dateActivated: datetime.datetime,
        stacked: bool = False,
    ) -> None:
        """Class for a booster.

        Args:
            _id (str): id of booster
            purchaserUuid (str): purchaser uuid
            amount (int): amount of boosters
            originalLength (int): original lenth
            length (int): length
            gameType (int): type of game applied to
            dateActivated (datetime.datetime): date activated
            stacked (bool, optional): wether stacked]. Defaults to False.
        """
        self._id = _id
        self.purchaserUuid = purchaserUuid
        self.amount = amount
        self.originalLength = originalLength
        self.length = length
        self.gameType = gameType
        self.dateActivated = dateActivated
        self.stacked = stacked


class Boosters:
    """Object containing boosters."""

    def __init__(self, boosterStatedecrementing: bool, boosters: List[Booster]) -> None:
        """Init object.

        Args:
            boosterStatedecrementing (bool): wether boosters stacked
            boosters (List[Booster]): list of boosters
        """
        self.boosterStatedecrementing = boosterStatedecrementing
        self.boosters = boosters
