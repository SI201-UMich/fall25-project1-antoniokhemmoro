# Name: Antonio Khemmoro 
# Student ID: 71867697
# Email: khemmoro@umich.edu
# Collaborators: Matthew Khemmoro
# Each wrote individual test cases
# AI usage: Used ChatGPT to help debug test cases and develop ideas for tests and help for creating them. 
import unittest
from superstore_analysis import (
    calculate_avg_sales_by_category,
    calculate_percent_profitable,
    calculate_avg_discount_by_region,
    calculate_percent_discounted,
)

class TestAntonio_AvgSalesByCategory(unittest.TestCase):
    def test_general_multiple_categories(self):
        rows = [
            {"Category": "Furniture", "Sales": 100.0, "Segment": "Consumer"},
            {"Category": "Furniture", "Sales": 300.0, "Segment": "Consumer"},
            {"Category": "Technology", "Sales": 200.0, "Segment": "Consumer"},
            {"Category": "Technology", "Sales": 100.0, "Segment": "Consumer"},
        ]
        self.assertEqual(
            calculate_avg_sales_by_category(rows),
            {"Furniture": 200.0, "Technology": 150.0},
        )

    def test_general_ignores_non_consumer(self):
        rows = [
            {"Category": "Furniture", "Sales": 100.0, "Segment": "Consumer"},
            {"Category": "Furniture", "Sales": 500.0, "Segment": "Corporate"},  # ignored
            {"Category": "Technology", "Sales": 200.0, "Segment": "Consumer"},
        ]
        self.assertEqual(
            calculate_avg_sales_by_category(rows),
            {"Furniture": 100.0, "Technology": 200.0},
        )

    def test_edge_ignores_na_and_blank_category(self):
        rows = [
            {"Category": "Furniture", "Sales": None, "Segment": "Consumer"},   # NA
            {"Category": "",          "Sales": 50.0,  "Segment": "Consumer"},  # blank category
            {"Category": "Furniture", "Sales": 100.0, "Segment": "Consumer"},
        ]
        self.assertEqual(calculate_avg_sales_by_category(rows), {"Furniture": 100.0})

    def test_edge_no_valid_rows_returns_empty_dict(self):
        rows = [
            {"Category": "Furniture", "Sales": None, "Segment": "Corporate"},
            {"Category": "",          "Sales": None, "Segment": "Consumer"},
        ]
        self.assertEqual(calculate_avg_sales_by_category(rows), {})


class TestAntonio_PercentProfitable(unittest.TestCase):
    def test_general_mixed_result(self):
        rows = [
            {"Profit": 10.0, "Quantity": 1, "Segment": "Consumer"},
            {"Profit": -1.0, "Quantity": 2, "Segment": "Corporate"},
            {"Profit":  0.0, "Quantity": 1, "Segment": "Consumer"},
            {"Profit":  5.0, "Quantity": 3, "Segment": "Corporate"},
            {"Profit":  2.0, "Quantity": 0, "Segment": "Consumer"},     # qty=0 ignored
            {"Profit":  3.0, "Quantity": 1, "Segment": "Home Office"},  # segment ignored
        ]
        # valid rows = 4; profitable = 2 -> 50%
        self.assertEqual(calculate_percent_profitable(rows), 50.0)

    def test_general_all_profitable_is_100(self):
        rows = [
            {"Profit": 1.0, "Quantity": 1, "Segment": "Consumer"},
            {"Profit": 2.0, "Quantity": 5, "Segment": "Corporate"},
        ]
        self.assertEqual(calculate_percent_profitable(rows), 100.0)

    def test_edge_zero_valid_rows_returns_zero(self):
        rows = [
            {"Profit": None, "Quantity": 1, "Segment": "Consumer"},
            {"Profit": 2.0,  "Quantity": 0, "Segment": "Corporate"},
            {"Profit": 3.0,  "Quantity": 2, "Segment": "Home Office"},
        ]
        self.assertEqual(calculate_percent_profitable(rows), 0.0)

    def test_edge_handles_missing_profit_and_qty(self):
        rows = [
            {"Profit": None, "Quantity": 2, "Segment": "Consumer"},
            {"Profit": 5.0,  "Quantity": None, "Segment": "Corporate"},
            {"Profit": 5.0,  "Quantity": 1, "Segment": "Corporate"},  # only valid
        ]
        self.assertEqual(calculate_percent_profitable(rows), 100.0)

# ADD MATTHEW'S TESTS
class TestMatthew_AvgDiscountByRegion(unittest.TestCase):
    def test_general_two_regions(self):
        rows = [
            {"Discount": 0.2, "Region": "West",  "Country": "United States"},
            {"Discount": 0.0, "Region": "West",  "Country": "United States"},
            {"Discount": 0.4, "Region": "East",  "Country": "United States"},
        ]
        self.assertEqual(
            calculate_avg_discount_by_region(rows),
            {"West": 0.1, "East": 0.4},
        )

    def test_general_ignores_non_us_rows(self):
        rows = [
            {"Discount": 0.3, "Region": "West", "Country": "Canada"},          # ignored
            {"Discount": 0.1, "Region": "West", "Country": "United States"},
        ]
        self.assertEqual(calculate_avg_discount_by_region(rows), {"West": 0.1})

    def test_edge_ignores_missing_discount_and_region(self):
        rows = [
            {"Discount": None, "Region": "West", "Country": "United States"},  # NA
            {"Discount": 0.2,  "Region": "",     "Country": "United States"},  # blank region
            {"Discount": 0.4,  "Region": "East", "Country": "United States"},
        ]
        self.assertEqual(calculate_avg_discount_by_region(rows), {"East": 0.4})

    def test_edge_no_valid_rows_returns_empty_dict(self):
        rows = [
            {"Discount": None, "Region": "", "Country": "United States"},
            {"Discount": 0.3,  "Region": "Central", "Country": "Canada"},
        ]
        self.assertEqual(calculate_avg_discount_by_region(rows), {})


class TestMatthew_PercentDiscounted(unittest.TestCase):

    def test_general_half_discounted(self):
        rows = [
            {"Discount": 0.0, "State": "California", "Sub-Category": "Chairs"},  # not discounted
            {"Discount": 0.2, "State": "California", "Sub-Category": "Chairs"},  # discounted
            {"Discount": 0.1, "State": "Texas",      "Sub-Category": "Phones"},  # discounted
            {"Discount": 0.0, "State": "New York",   "Sub-Category": "Paper"},   # not discounted
        ]
        self.assertEqual(calculate_percent_discounted(rows), 50.0)

    def test_general_all_discounted_is_100(self):
        rows = [
            {"Discount": 0.05, "State": "Florida", "Sub-Category": "Binders"},
            {"Discount": 0.10, "State": "Texas",   "Sub-Category": "Phones"},
        ]
        self.assertEqual(calculate_percent_discounted(rows), 100.0)

    def test_edge_missing_discount_excluded_from_denominator(self):
        rows = [
            {"Discount": None, "State": "California", "Sub-Category": "Chairs"},  # excluded
            {"Discount": 0.0,  "State": "California", "Sub-Category": "Chairs"},  # counted, not discounted
            {"Discount": 0.2,  "State": "California", "Sub-Category": "Chairs"},  # counted, discounted
        ]
        self.assertEqual(calculate_percent_discounted(rows), 50.0)

    def test_edge_no_qualifying_rows_returns_zero(self):
        rows = [
            {"Discount": 0.2, "State": "Ohio",  "Sub-Category": "Paper"},   # state not allowed
            {"Discount": 0.3, "State": "Texas", "Sub-Category": "Tables"},  # subcat not allowed
            {"Discount": None,"State": "New York","Sub-Category": "Phones"},# NA -> excluded
        ]
        self.assertEqual(calculate_percent_discounted(rows), 0.0)


if __name__ == "__main__":
    unittest.main()
