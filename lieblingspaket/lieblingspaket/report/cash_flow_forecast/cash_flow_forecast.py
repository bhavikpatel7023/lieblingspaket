# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate, now

def execute(filters=None):
	columns, data = [], []
	if not filters: filters = {}
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))

	if not filters.get("to_date"):
		frappe.throw(_("'To Date' is required"))
	
	columns = get_columns()
	data = get_data(filters)
	
	return columns, data
	
	
def get_columns():
	"""return columns"""

	columns = [
		_("Order No")+":Link/Sales Order:150",
		_("Date of Payment ")+":Data:150",
		_("Amount of Payment")+":Float:150",
		_("Currency of Payment")+":Link/Currency:150"		
	]

	return columns
	
	
def get_data(filters):
	"""return data"""
	return frappe.db.sql("""select schedule.parent,schedule.due_date,schedule.payment_amount,sorder.currency from `tabPayment Schedule` as schedule INNER JOIN `tabPurchase Order` as sorder ON schedule.parent = sorder.name and sorder.docstatus=1 and ( schedule.due_date between %s and %s ) order by schedule.due_date asc ;""",(filters.get("from_date"),filters.get("to_date")))

