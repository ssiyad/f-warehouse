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
            "fieldname": "quantity_before",
            "fieldtype": "Int",
            "label": "Quantity Before",
        },
        {
            "fieldname": "quantity_change",
            "fieldtype": "Int",
            "label": "Change in Quantity",
        },
        {
            "fieldname": "quantity_after",
            "fieldtype": "Int",
            "label": "Quantity After",
        },
        {
            "fieldname": "unit_value",
            "fieldtype": "Currency",
            "label": "Value per Unit",
        },
        {
            "fieldname": "value_change",
            "fieldtype": "Currency",
            "label": "Change in Value",
        },
    ]

    if filters and "date_from" in filters:
        filters["modified"] = [">", filters["date_from"]]
        del filters["date_from"]

    if filters and "date_to" in filters:
        filters["modified"] = ["<", filters["date_to"]]
        del filters["date_to"]

    data = frappe.db.get_list("Warehouse Ledger", filters=filters, fields="*")

    for row in data:
        row["quantity_before"] = (
            frappe.db.get_value(
                "Warehouse Ledger",
                {**filters, "modified": ["<", row.modified]},
                "sum(quantity_change)",
            )
            or 0
        )
        row["quantity_after"] = row["quantity_before"] + row["quantity_change"]
        row["unit_value"] = row["value_change"] / row["quantity_change"]

    return columns, data
