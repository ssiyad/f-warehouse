# Copyright (c) 2022, Sabu Siyad and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document, frappe

class StockEntry(Document):
	def before_submit(self):
		if self.type == "Transfer" and self.from_warehouse is None:
			frappe.throw("From Warehouse must not be for stock transfer")

		if self.from_warehouse == self.warehouse:
			frappe.throw("Source and destination warehouses must not be same")

	@staticmethod
	def create_ledger_entry(item, warehouse, quantity_change, value_change):
		d = frappe.new_doc("Warehouse Ledger")
		d.item = item
		d.warehouse = warehouse
		d.quantity_change = quantity_change
		d.value_change = value_change
		d.save()

	def on_submit(self):
		self.create_ledger_entry(self.item, self.warehouse, self.quantity, 0)

		if self.from_warehouse is not None:
			self.create_ledger_entry(self.item, self.from_warehouse, self.quantity * -1, 0)

	def on_cancel(self):
		self.create_ledger_entry(self.item, self.warehouse, self.quantity * -1, 0)

		if self.from_warehouse is not None:
			self.create_ledger_entry(self.item, self.from_warehouse, self.quantity, 0)

