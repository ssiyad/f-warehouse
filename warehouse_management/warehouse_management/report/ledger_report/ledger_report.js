// Copyright (c) 2022, Sabu Siyad and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ledger Report"] = {
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.id == "value_change" && data) {
			color = data.value_change < 0 ? "red" : "green";
			value = `<span style='color:${color};'>${value}</span>`;
		}

		return value;
	},
};
