# Copyright (c) 2022, Sabu Siyad and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
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
            "fieldname": "quantity_balance",
            "fieldtype": "Int",
            "label": "Balance Quantity",
        },
        {
            "fieldname": "value_balance",
            "fieldtype": "Currency",
            "label": "Balance Value",
        },
    ]

    if filters and "date" in filters:
        filters["modified"] = ["<=", filters["date"]]
        del filters["date"]

    fields = ["item", "warehouse", "modified"]
    group_by = "warehouse, item"

    data = frappe.db.get_list(
        "Warehouse Ledger", filters=filters, fields=fields, group_by=group_by
    )

    for i, row in enumerate(data):
        _filters = {
            **filters,
            "warehouse": row.warehouse,
            "item": row.item,
            "modified": ["<=", row.modified],
        }

        _fields = [
            "item",
            "warehouse",
            "sum(quantity_change) as quantity_balance",
            "sum(value_change) as value_balance",
        ]

        data[i] = frappe.db.get_value(
            "Warehouse Ledger",
            _filters,
            _fields,
            as_dict=True,
        )

    return columns, data
