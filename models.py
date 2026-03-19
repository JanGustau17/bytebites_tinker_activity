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
        # Return the sum of prices for all items selected in this transaction.
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

    def compute_lifetime_total_spent(self) -> float:
        # Return total amount spent across all past transactions for this customer.
        return sum(txn.compute_total_cost() for txn in self.past_purchase_history)


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
        # Return all items whose category matches the requested category.
        requested_category = category.strip().lower()
        if not requested_category:
            return []
        return [
            item
            for item in self.all_items
            if item.category.strip().lower() == requested_category
        ]

    def sort_items_by_name(self, desc: bool = False) -> List[FoodItem]:
        # Return items sorted alphabetically by name.
        return sorted(self.all_items, key=lambda item: item.name.lower(), reverse=desc)

    def sort_items_by_price(self, desc: bool = False) -> List[FoodItem]:
        # Return items sorted by price from low-to-high, or high-to-low if desc=True.
        return sorted(self.all_items, key=lambda item: item.price, reverse=desc)

    def sort_items_by_popularity(self, desc: bool = True) -> List[FoodItem]:
        # Return items sorted by popularity rating (most popular first by default).
        return sorted(
            self.all_items,
            key=lambda item: item.popularity_rating,
            reverse=desc,
        )


def _demo_models_scenario() -> None:
    menu = Menu()
    menu.add_item(FoodItem("Spicy Burger", 8.99, "Meals", 5))
    menu.add_item(FoodItem("Large Soda", 2.50, "Drinks", 4))
    menu.add_item(FoodItem("Chocolate Cake", 4.00, "Desserts", 5))
    menu.add_item(FoodItem("Iced Tea", 2.75, "Drinks", 2))

    drinks = menu.filter_by_category("drinks")
    by_name = menu.sort_items_by_name()
    by_price_desc = menu.sort_items_by_price(desc=True)
    by_popularity = menu.sort_items_by_popularity()

    order = Transaction([drinks[0], by_name[0]])
    customer = Customer("Demo User", [order])

    print("--- models.py scenario ---")
    print("Filtered drinks:", [item.name for item in drinks])
    print("Sorted by name:", [item.name for item in by_name])
    print("Sorted by price desc:", [item.name for item in by_price_desc])
    print("Sorted by popularity:", [item.name for item in by_popularity])
    print(f"Order total: ${order.compute_total_cost():.2f}")
    print(f"Lifetime total: ${customer.compute_lifetime_total_spent():.2f}")


if __name__ == "__main__":
    _demo_models_scenario()
