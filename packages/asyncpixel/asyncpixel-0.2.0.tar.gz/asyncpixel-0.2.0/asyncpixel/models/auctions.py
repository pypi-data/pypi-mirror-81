"""Auction related objects."""

import datetime
from typing import List


class Auction_item:
    """auction item class."""

    def __init__(
        self,
        uuid: str,
        auctioneer: str,
        profile_id: str,
        coop: List[str],
        start: datetime.datetime,
        end: datetime.datetime,
        item_name: str,
        item_lore: str,
        extra: str,
        category: str,
        tier: str,
        starting_bid: int,
        item_bytes: str,
        claimed: bool,
        claimed_bidders: List,
        highest_bid_amount: int,
        bids: List,
        _id: str = None,
    ) -> None:
        """Auction Object.

        Args:
            uuid (str): UUID of Auction.
            auctioneer (str): UUID of Auctioneer.
            profile_id (str): UUID of the player.
            coop (List[str]): coop.
            start (datetime.datetime): Auction start time.
            end (datetime.datetime): Auction end time.
            item_name (str): Name of the item for auction.
            item_lore (str): Lore of the item for auction.
            extra (str): Extra information about the item for auction.
            category (str): The category the item is in.
            tier (str): The tier of the item.
            starting_bid (int): Starting bid of the item.
            item_bytes (str): item_bytes.
            claimed (bool): If the item has been claimed.
            claimed_bidders (List): List of bidders who have claimed the item.
            highest_bid_amount (int): Highest amount bid on the iteam.
            bids (List): List of bids on the item.
            _id (str, optional): _id of the auction. Defaults to None.
        """
        self.id = _id
        self.uuid = uuid
        self.auctioneer = auctioneer
        self.profile_id = profile_id
        self.coop = coop
        self.start = start
        self.end = end
        self.item_name = item_name
        self.item_lore = item_lore
        self.extra = extra
        self.category = category
        self.tier = tier
        self.starting_bid = starting_bid
        self.item_bytes = item_bytes
        self.claimed = claimed
        self.claimed_bidders = claimed_bidders
        self.highest_bid_amount = highest_bid_amount
        self.bids = bids


class Auction:
    """Main auction object."""

    def __init__(
        self,
        page: str,
        totalPages: str,
        totalAuctions: str,
        lastUpdated: datetime.datetime,
        auctions: List[Auction_item],
    ) -> None:
        """Init main object.

        Args:
            page (str): Current page number.
            totalPages (str): Total pages.
            totalAuctions (str): Total auctions.
            lastUpdated (datetime.datetime): When data was last updated
            auctions (List[Auction_item]): List of auctions
        """
        self.page = page
        self.totalPages = totalPages
        self.totalAuctions = totalAuctions
        self.lastUpdated = lastUpdated
        self.auctions = auctions
