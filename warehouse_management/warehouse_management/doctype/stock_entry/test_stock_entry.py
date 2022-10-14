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
    def setup_item(self):
        return frappe.get_doc(
            {
                "doctype": "Item",
                "item_name": TEST_ITEM_NAME,
            }
        ).insert()

    def drop_item(self):
        frappe.delete_doc_if_exists("Item", TEST_ITEM_NAME)

    def get_item(self):
        return frappe.get_last_doc("Item", {"item_name": TEST_ITEM_NAME})

    def setup_warehouse(self):
        return frappe.get_doc(
            {
                "doctype": "Warehouse",
                "warehouse_name": TEST_WAREHOUSE_NAME,
            }
        ).insert()

    def drop_warehouse(self):
        frappe.delete_doc_if_exists("Warehouse", TEST_WAREHOUSE_NAME)

    def get_warehouse(self):
        return frappe.get_last_doc("Warehouse", {"warehouse_name": TEST_WAREHOUSE_NAME})

    def setUp(self):
        self.setup_item()
        self.setup_warehouse()

    def tearDown(self):
        self.drop_item()
        self.drop_warehouse()

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
