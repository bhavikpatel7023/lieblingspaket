# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate, now

def execute(filters=None):
	if not filters: filters = {}
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))

	if not filters.get("to_date"):
		frappe.throw(_("'To Date' is required"))

	conditions, filters = get_conditions(filters)
	columns = get_column()
	data = get_data(conditions,filters)
	return columns,data
	
	
def get_column():
	return [_("Date")+":Date:80",
		_("Item Code")+":Link/Item:80",
		_("Item Name")+"::120",
		_("No Of Export Carton")+":Float:80",
		_("Number of Palettes")+":Float:80",
		_("Volume in CBM")+":Float:80",
		_("Weight in Kg")+":Float:80",
		_("Warehouse")+":Link/Warehouse:80",
		_("Order Qty")+":Float:80",
		_("Received Qty")+":Float:80"
	]
	
def get_data(conditions,filters):
	po = frappe.db.sql(""" select o2.transaction_date, o1.item_code, o1.item_name, o1.number_of_export_carton, o1.number_of_palette, o1.volume_in_cbm, o1.weight_in_kg, o1.warehouse, o1.qty, ifnull(o1.received_qty,"0.00") from `tabPurchase Order Item` o1, `tabPurchase Order` o2 where (o1.parent = o2.name) and (o2.status ='To Receive and Bill') %s;"""%conditions, filters, as_list=1)
	return po

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"): conditions += " and o2.transaction_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and o2.transaction_date <= %(to_date)s"
	if filters.get("item_code"): conditions = "and o1.item_code = %(item_code)s"
	if filters.get("warehouse"): conditions = "and o1.warehouse = %(warehouse)s"

	return conditions, filters

