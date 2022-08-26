# Copyright (c) 2018, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.utils import getdate, today


def execute():
	"""Generates leave ledger entries for leave allocation/application/encashment
	for last allocation"""
	finergy.reload_doc("HR", "doctype", "Leave Ledger Entry")
	finergy.reload_doc("HR", "doctype", "Leave Encashment")
	finergy.reload_doc("HR", "doctype", "Leave Type")

	if not finergy.get_meta("Leave Allocation").has_field("unused_leaves"):
		finergy.reload_doc("HR", "doctype", "Leave Allocation")
		update_leave_allocation_fieldname()

	generate_allocation_ledger_entries()
	generate_application_leave_ledger_entries()
	generate_encashment_leave_ledger_entries()
	generate_expiry_allocation_ledger_entries()


def update_leave_allocation_fieldname():
	"""maps data from old field to the new field"""
	finergy.db.sql(
		"""
		UPDATE `tabLeave Allocation`
		SET `unused_leaves` = `carry_forwarded_leaves`
	"""
	)


def generate_allocation_ledger_entries():
	"""fix ledger entries for missing leave allocation transaction"""
	allocation_list = get_allocation_records()

	for allocation in allocation_list:
		if not finergy.db.exists(
			"Leave Ledger Entry",
			{"transaction_type": "Leave Allocation", "transaction_name": allocation.name},
		):
			allocation_obj = finergy.get_doc("Leave Allocation", allocation)
			allocation_obj.create_leave_ledger_entry()


def generate_application_leave_ledger_entries():
	"""fix ledger entries for missing leave application transaction"""
	leave_applications = get_leaves_application_records()

	for application in leave_applications:
		if not finergy.db.exists(
			"Leave Ledger Entry",
			{"transaction_type": "Leave Application", "transaction_name": application.name},
		):
			finergy.get_doc("Leave Application", application.name).create_leave_ledger_entry()


def generate_encashment_leave_ledger_entries():
	"""fix ledger entries for missing leave encashment transaction"""
	leave_encashments = get_leave_encashment_records()

	for encashment in leave_encashments:
		if not finergy.db.exists(
			"Leave Ledger Entry",
			{"transaction_type": "Leave Encashment", "transaction_name": encashment.name},
		):
			finergy.get_doc("Leave Encashment", encashment).create_leave_ledger_entry()


def generate_expiry_allocation_ledger_entries():
	"""fix ledger entries for missing leave allocation transaction"""
	from capkpi.hr.doctype.leave_ledger_entry.leave_ledger_entry import expire_allocation

	allocation_list = get_allocation_records()

	for allocation in allocation_list:
		if not finergy.db.exists(
			"Leave Ledger Entry",
			{"transaction_type": "Leave Allocation", "transaction_name": allocation.name, "is_expired": 1},
		):
			allocation_obj = finergy.get_doc("Leave Allocation", allocation)
			if allocation_obj.to_date <= getdate(today()):
				expire_allocation(allocation_obj)


def get_allocation_records():
	return finergy.get_all(
		"Leave Allocation", filters={"docstatus": 1}, fields=["name"], order_by="to_date ASC"
	)


def get_leaves_application_records():
	return finergy.get_all("Leave Application", filters={"docstatus": 1}, fields=["name"])


def get_leave_encashment_records():
	return finergy.get_all("Leave Encashment", filters={"docstatus": 1}, fields=["name"])
