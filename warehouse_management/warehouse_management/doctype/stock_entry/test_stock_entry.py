# Copyright (c) 2022, Sabu Siyad and Contributors
# See license.txt

import random
import string

import frappe
from frappe.tests.utils import FrappeTestCase


def random_string():
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )


TEST_ITEM_NAME = random_string()
TEST_WAREHOUSE_NAME = random_string()


class TestStockEntry(FrappeTestCase):
    @staticmethod
    def setup_item():
        if frappe.flags.test_item_created:
            return

        d = frappe.get_doc(
            {
                "doctype": "Item",
                "item_name": TEST_ITEM_NAME,
            }
        ).insert()

        frappe.flags.test_item_created = True

        return d

    @staticmethod
    def drop_item():
        frappe.delete_doc_if_exists("Item", {"item_name": TEST_ITEM_NAME})

    @staticmethod
    def get_item():
        return frappe.get_last_doc("Item", {"item_name": TEST_ITEM_NAME})

    @staticmethod
    def setup_warehouse():
        if frappe.flags.test_warehouse_created:
            return

        d = frappe.get_doc(
            {
                "doctype": "Warehouse",
                "warehouse_name": TEST_WAREHOUSE_NAME,
            }
        ).insert()

        frappe.flags.test_warehouse_created = True

        return d

    @staticmethod
    def drop_warehouse():
        frappe.delete_doc_if_exists(
            "Warehouse", {"warehouse_name": TEST_WAREHOUSE_NAME}
        )

    @staticmethod
    def get_warehouse():
        return frappe.get_last_doc("Warehouse", {"warehouse_name": TEST_WAREHOUSE_NAME})

    @staticmethod
    def drop_stock_entry():
        frappe.delete_doc_if_exists(
            "Stock Entry", {"item": TEST_ITEM_NAME, "warehouse": TEST_WAREHOUSE_NAME}
        )

    @staticmethod
    def drop_moving_average():
        frappe.delete_doc_if_exists(
            "Moving Average", {"item": TEST_ITEM_NAME, "warehouse": TEST_WAREHOUSE_NAME}
        )

    def setUp(self):
        self.setup_item()
        self.setup_warehouse()

    def tearDown(self):
        self.drop_item()
        self.drop_warehouse()
        self.drop_moving_average()
        self.drop_stock_entry()

    def test_moving_average(self):
        item = self.get_item()
        warehouse = self.get_warehouse()
        total_price = total_quantity = 0

        for _ in range(random.randint(3, 10)):
            quantity = random.randint(10, 100)
            price = random.randint(10, 100)

            frappe.get_doc(
                {
                    "doctype": "Stock Entry",
                    "type": "Receipt",
                    "item": item.name,
                    "warehouse": warehouse.name,
                    "quantity": quantity,
                    "price": price,
                }
            ).submit()

            total_price += price * quantity
            total_quantity += quantity

        d = frappe.get_value(
            "Moving Average",
            filters={"item": item.name, "warehouse": warehouse.name},
            fieldname=["price", "quantity"],
            as_dict=True,
        )

        self.assertAlmostEqual(d["price"], total_price / total_quantity)
        self.assertEqual(d["quantity"], total_quantity)

    def test_transfer_same_warehouse(self):
        item = self.get_item()
        warehouse = self.get_warehouse()

        entry = frappe.get_doc(
            {
                "doctype": "Stock Entry",
                "type": "Transfer",
                "item": item.name,
                "warehouse": warehouse.name,
                "from_warehouse": warehouse.name,
                "quantity": random.randint(10, 100),
                "price": random.randint(10, 100),
            }
        )

        try:
            entry.submit()
            entry.delete()
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, frappe.exceptions.ValidationError)
