// Copyright (c) 2022, Sabu Siyad and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Balance"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": "Date",
			"fieldtype": "Datetime",
			"default": "Today"
		},
		{
			"fieldname": "item",
			"label": "Item",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "warehouse",
			"label": "Warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
		},
	],
	// "formatter": function(value, row, column, data, default_formatter) {
	// 	value = default_formatter(value, row, column, data);

	// 	if (column.id === "value_balance") {
	// 		color = data?.value_balance < data?.value_opening ? "red" : "green";
	// 		value = `<span style='color:${color};'>${value}</span>`;
	// 	}

	// 	if (row === undefined && column.id === "value_balance") {
	// 		value = ""
	// 	}

	// 	return value;
	// },
};
