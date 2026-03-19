import unittest

from models import FoodItem, Menu, Transaction


class TestByteBitesCoreBehaviors(unittest.TestCase):
	def test_order_total_with_items(self) -> None:
		transaction = Transaction(
			[
				FoodItem("Spicy Burger", 10.0, "Meals", 5),
				FoodItem("Large Soda", 5.0, "Drinks", 4),
			]
		)
		self.assertAlmostEqual(transaction.compute_total_cost(), 15.0, places=2)

	def test_order_total_is_zero_when_empty(self) -> None:
		transaction = Transaction([])
		self.assertEqual(transaction.compute_total_cost(), 0)

	def test_filter_menu_items_by_category_case_insensitive(self) -> None:
		menu = Menu(
			[
				FoodItem("Large Soda", 2.5, "Drinks", 4),
				FoodItem("Chocolate Cake", 4.0, "Desserts", 5),
				FoodItem("Iced Tea", 2.75, "drinks", 3),
			]
		)

		drinks = menu.filter_by_category("DRINKS")
		self.assertEqual(len(drinks), 2)
		self.assertEqual([item.name for item in drinks], ["Large Soda", "Iced Tea"])
		self.assertTrue(all(item.category.lower() == "drinks" for item in drinks))


if __name__ == "__main__":
	unittest.main()
