"""Bazaar classes."""

import datetime
from typing import List


class Bazaar_buy_summary:
    """Bazaar buy object."""

    def __init__(self, amount: int, pricePerUnit: int, orders: int) -> None:
        """Init object.

        Args:
            amount (int): Amount.
            pricePerUnit (int): Price Per Unit.
            orders (int): Amount of orders.
        """
        self.amount = amount
        self.pricePerUnit = pricePerUnit
        self.orders = orders


class Bazaar_sell_summary:
    """Bazaar sell object."""

    def __init__(self, amount: int, pricePerUnit: int, orders: int) -> None:
        """Init object.

        Args:
            amount (int): Amount.
            pricePerUnit (int): Price Per Unit.
            orders (int): How many orders.
        """
        self.amount = amount
        self.pricePerUnit = pricePerUnit
        self.orders = orders


class Bazaar_quick_status:
    """Bazaar quick status."""

    def __init__(
        self,
        productId: str,
        sellPrice: float,
        sellVolume: int,
        sellMovingWeek: int,
        sellOrders: int,
        buyPrice: float,
        buyVolume: int,
        buyMovingWeek: int,
        buyOrders: int,
    ) -> None:
        """Init object.

        Args:
            productId (str): ID of the product being sold.
            sellPrice (float): Weighted average of the top 2%
                of orders by volume.
            sellVolume (int):  Sum of item amounts in all orders.
            sellMovingWeek (int): Volume sold in the last 7 days + live.
            sellOrders (int): Count of current orders.
            buyPrice (float): Weighted average of the top 2%
                of orders by volume.
            buyVolume (int): Sum of item amounts in all orders.
            buyMovingWeek (int): Volume sold in the last 7 days + live.
            buyOrders (int): count of current orders.
        """
        self.productId = productId
        self.sellPrice = sellPrice
        self.sellVolume = sellVolume
        self.sellMovingWeek = sellMovingWeek
        self.sellOrders = sellOrders
        self.buyPrice = sellPrice
        self.buyVolume = sellVolume
        self.buyMovingWeek = sellMovingWeek
        self.buyOrders = sellOrders


class Bazaar:
    """Bazaar object."""

    def __init__(self, lastUpdated: datetime.datetime, bazaar_items: List) -> None:
        """Init object.

        Args:
            lastUpdated (datetime.datetime): dateTime of when the data
                was last updated.
            bazaar_items (List): List of Bazaar items
        """
        self.lastUpdated = lastUpdated
        self.bazaar_items = bazaar_items


class Bazaar_item:
    """Bazaar item."""

    def __init__(
        self,
        name: str,
        product_id: str,
        sell_summary: List[Bazaar_sell_summary],
        buy_summary: List[Bazaar_buy_summary],
        quick_status: Bazaar_quick_status,
    ) -> None:
        """Init object.

        Args:
            name (str): Name of the product being sold.
            product_id (str): Product ID of item being sold.
            sell_summary (Bazaar_sell_summary): List of current top 30 orders
                for this product.
            buy_summary (Bazaar_buy_summary): List of current top 30 orders
                for this product.
            quick_status (Bazaar_quick_status): Computed summary of live
                state of the product.
        """
        self.name = name
        self.product_id = product_id
        self.sell_summary = sell_summary
        self.buy_summary = buy_summary
        self.quick_status = quick_status
