# Copyright (c) 2022, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{
			"fieldname": "modified",
			"fieldtype": "Datetime",
			"label": "Date",
		},
		{
			"fieldname": "item",
			"fieldtype": "Link",
			"label": "Item",
			"options": "Item",
		},
		{
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"label": "Warehouse",
			"options": "Warehouse",
		},
		{
			"fieldname": "quantity_change",
			"fieldtype": "Int",
			"label": "Change in Quantity",
			"indicator": "Green"
		},
		{
			"fieldname": "value_change",
			"fieldtype": "Currency",
			"label": "Change in Value",
		},
	]

	data = frappe.db.get_list("Warehouse Ledger", filters=filters, fields="*")

	return columns, data
