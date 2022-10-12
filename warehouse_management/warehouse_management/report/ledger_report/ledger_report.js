// Copyright (c) 2022, Sabu Siyad and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ledger Report"] = {
	"filters": [
		{
			"fieldname": "date_from",
			"label": "From Date",
			"fieldtype": "Datetime",
		},
		{
			"fieldname": "date_to",
			"label": "To Date",
			"fieldtype": "Datetime",
		},
		{
			"fieldname": "item",
			"label": "Item",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "Warehouse",
			"label": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
		},
		{
			"fieldname": "stock_entry",
			"label": "Stock Entry",
			"fieldtype": "Link",
			"options": "Stock Entry",
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (["value_change", "quantity_change"].includes(column.id) && data) {
			color = data.value_change < 0 ? "red" : "green";
			value = `<span style='color:${color};'>${value}</span>`;
		}

		if (row === undefined && column.id === "unit_value") {
			value = ""
		}

		return value;
	},
};
