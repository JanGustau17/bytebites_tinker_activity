"""ByteBites backend models.

Classes:
- Customer: stores customer identity and purchase history, and verifies basic user validity.
- FoodItem: represents a menu item with name, price, category, and popularity rating.
- Menu: holds the full item collection and supports category-based filtering.
- Transaction: groups selected items and computes total purchase cost.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class FoodItem:
    name: str
    price: float
    category: str
    popularity_rating: int

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.category = self.category.strip()
        if not self.name:
            raise ValueError("FoodItem name cannot be empty")
        if not self.category:
            raise ValueError("FoodItem category cannot be empty")
        if self.price < 0:
            raise ValueError("FoodItem price cannot be negative")
        if not 1 <= self.popularity_rating <= 5:
            raise ValueError("FoodItem popularity_rating must be between 1 and 5")


@dataclass
class Transaction:
    selected_items: List[FoodItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not all(isinstance(item, FoodItem) for item in self.selected_items):
            raise TypeError("Transaction selected_items must contain only FoodItem")

    def compute_total_cost(self) -> float:
        return sum(item.price for item in self.selected_items)


@dataclass
class Customer:
    name: str
    past_purchase_history: List[Transaction] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if any(not isinstance(txn, Transaction) for txn in self.past_purchase_history):
            raise TypeError(
                "Customer past_purchase_history must contain only Transaction"
            )

    def verify_user(self) -> bool:
        has_valid_name = bool(self.name and self.name.strip())
        has_purchase_history = len(self.past_purchase_history) > 0
        return has_valid_name and has_purchase_history


@dataclass
class Menu:
    all_items: List[FoodItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not all(isinstance(item, FoodItem) for item in self.all_items):
            raise TypeError("Menu all_items must contain only FoodItem")

    def add_item(self, item: FoodItem) -> None:
        if not isinstance(item, FoodItem):
            raise TypeError("Menu can only add FoodItem instances")
        self.all_items.append(item)

    def filter_by_category(self, category: str) -> List[FoodItem]:
        requested_category = category.strip().lower()
        if not requested_category:
            return []
        return [
            item
            for item in self.all_items
            if item.category.strip().lower() == requested_category
        ]
