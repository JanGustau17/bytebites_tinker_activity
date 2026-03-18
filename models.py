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


@dataclass
class Transaction:
    selected_items: List[FoodItem] = field(default_factory=list)

    def compute_total_cost(self) -> float:
        return sum(item.price for item in self.selected_items)


@dataclass
class Customer:
    name: str
    past_purchase_history: List[Transaction] = field(default_factory=list)

    def verify_user(self) -> bool:
        has_valid_name = bool(self.name and self.name.strip())
        has_purchase_history = len(self.past_purchase_history) > 0
        return has_valid_name and has_purchase_history


@dataclass
class Menu:
    all_items: List[FoodItem] = field(default_factory=list)

    def add_item(self, item: FoodItem) -> None:
        self.all_items.append(item)

    def filter_by_category(self, category: str) -> List[FoodItem]:
        requested_category = category.strip().lower()
        return [
            item
            for item in self.all_items
            if item.category.strip().lower() == requested_category
        ]
