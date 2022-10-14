# Copyright (c) 2022, Sabu Siyad and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document, frappe


class StockEntry(Document):
    @staticmethod
    def create_ledger_entry(stock_entry, item, warehouse, quantity_change, value_change):
        d = frappe.new_doc("Warehouse Ledger")
        d.stock_entry = stock_entry
        d.item = item
        d.warehouse = warehouse
        d.quantity_change = quantity_change
        d.value_change = value_change
        return d.save()

    @staticmethod
    def recalc_moving_average(item, warehouse, quantity, price):
        d = frappe.db.get_value(
            "Moving Average",
            {"item": item, "warehouse": warehouse},
            ["name", "price", "quantity"],
            as_dict=True,
        )
        if d:
            q = d.quantity + quantity
            p = ((d.price * d.quantity) + (quantity * price)) / q
            frappe.db.set_value("Moving Average", d.name, {"quantity": q, "price": p})
            return

        new_d = frappe.new_doc("Moving Average")
        new_d.item = item
        new_d.warehouse = warehouse
        new_d.price = price
        new_d.quantity = quantity
        return new_d.insert()

    @staticmethod
    def get_moving_average(item, warehouse):
        return frappe.get_value(
            "Moving Average", {"item": item, "warehouse": warehouse}, "price"
        )

    @staticmethod
    def ensure_quantity(item, warehouse, quantity):
        available_q = (
            frappe.db.get_value(
                "Warehouse Ledger",
                {"warehouse": warehouse, "item": item},
                "sum(quantity_change)",
            )
            or 0
        )

        if available_q < quantity:
            frappe.throw("Insufficient quantity")

    def before_submit(self):
        if self.type == "Transfer" and self.from_warehouse is None:
            frappe.throw("From Warehouse must not be empty for stock transfer")

        if self.from_warehouse == self.warehouse:
            frappe.throw("Source and destination warehouses must not be same")

        if self.type == "Transfer" and self.from_warehouse:
            self.ensure_quantity(self.item, self.from_warehouse, self.quantity)

        if self.type == "Consume":
            self.ensure_quantity(self.item, self.warehouse, self.quantity)

    def receipt(self, warehouse=None):
        self.create_ledger_entry(
            self.name,
            self.item,
            warehouse or self.warehouse,
            self.quantity,
            self.quantity * self.price,
        )

        self.recalc_moving_average(
            self.item, warehouse or self.warehouse, self.quantity, self.price
        )

    def consume(self, warehouse=None):
        value = self.get_moving_average(self.item, warehouse or self.warehouse)

        self.create_ledger_entry(
            self.name,
            self.item,
            warehouse or self.warehouse,
            self.quantity * -1,
            self.quantity * -1 * value,
        )

    def transfer(self):
        self.receipt(self.warehouse)
        self.consume(self.from_warehouse)

    def on_submit(self):
        match self.type.lower():
            case "receipt":
                self.receipt()
            case "consume":
                self.consume()
            case "transfer":
                self.transfer()

    def before_cancel(self):
        frappe.throw("Can not cancel")
