# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import random
from datetime import timedelta

import finergy
from finergy.desk import query_report
from finergy.utils.make_random import how_many

import capkpi
from capkpi.manufacturing.doctype.work_order.test_work_order import make_wo_order_test_record


def work():
	if random.random() < 0.3:
		return

	finergy.set_user(finergy.db.get_global("demo_manufacturing_user"))
	if not finergy.get_all("Sales Order"):
		return

	ppt = finergy.new_doc("Production Plan")
	ppt.company = capkpi.get_default_company()
	# ppt.use_multi_level_bom = 1 #refactored
	ppt.get_items_from = "Sales Order"
	# ppt.purchase_request_for_warehouse = "Stores - WPL" # refactored
	ppt.run_method("get_open_sales_orders")
	if not ppt.get("sales_orders"):
		return
	ppt.run_method("get_items")
	ppt.run_method("raise_material_requests")
	ppt.save()
	ppt.submit()
	ppt.run_method("raise_work_orders")
	finergy.db.commit()

	# submit work orders
	for pro in finergy.db.get_values("Work Order", {"docstatus": 0}, "name"):
		b = finergy.get_doc("Work Order", pro[0])
		b.wip_warehouse = "Work in Progress - WPL"
		b.submit()
		finergy.db.commit()

	# submit material requests
	for pro in finergy.db.get_values("Material Request", {"docstatus": 0}, "name"):
		b = finergy.get_doc("Material Request", pro[0])
		b.submit()
		finergy.db.commit()

	# stores -> wip
	if random.random() < 0.4:
		for pro in query_report.run("Open Work Orders")["result"][: how_many("Stock Entry for WIP")]:
			make_stock_entry_from_pro(pro[0], "Material Transfer for Manufacture")

	# wip -> fg
	if random.random() < 0.4:
		for pro in query_report.run("Work Orders in Progress")["result"][
			: how_many("Stock Entry for FG")
		]:
			make_stock_entry_from_pro(pro[0], "Manufacture")

	for bom in finergy.get_all("BOM", fields=["item"], filters={"with_operations": 1}):
		pro_order = make_wo_order_test_record(
			item=bom.item,
			qty=2,
			source_warehouse="Stores - WPL",
			wip_warehouse="Work in Progress - WPL",
			fg_warehouse="Stores - WPL",
			company=capkpi.get_default_company(),
			stock_uom=finergy.db.get_value("Item", bom.item, "stock_uom"),
			planned_start_date=finergy.flags.current_date,
		)

	# submit job card
	if random.random() < 0.4:
		submit_job_cards()


def make_stock_entry_from_pro(pro_id, purpose):
	from capkpi.manufacturing.doctype.work_order.work_order import make_stock_entry
	from capkpi.stock.doctype.stock_entry.stock_entry import (
		DuplicateEntryForWorkOrderError,
		IncorrectValuationRateError,
		OperationsNotCompleteError,
	)
	from capkpi.stock.stock_ledger import NegativeStockError

	try:
		st = finergy.get_doc(make_stock_entry(pro_id, purpose))
		st.posting_date = finergy.flags.current_date
		st.fiscal_year = str(finergy.flags.current_date.year)
		for d in st.get("items"):
			d.cost_center = "Main - " + finergy.get_cached_value("Company", st.company, "abbr")
		st.insert()
		finergy.db.commit()
		st.submit()
		finergy.db.commit()
	except (
		NegativeStockError,
		IncorrectValuationRateError,
		DuplicateEntryForWorkOrderError,
		OperationsNotCompleteError,
	):
		finergy.db.rollback()


def submit_job_cards():
	work_orders = finergy.get_all(
		"Work Order", ["name", "creation"], {"docstatus": 1, "status": "Not Started"}
	)
	work_order = random.choice(work_orders)
	# for work_order in work_orders:
	start_date = work_order.creation
	work_order = finergy.get_doc("Work Order", work_order.name)
	job = finergy.get_all(
		"Job Card", ["name", "operation", "work_order"], {"docstatus": 0, "work_order": work_order.name}
	)

	if not job:
		return
	job_map = {}
	for d in job:
		job_map[d.operation] = finergy.get_doc("Job Card", d.name)

	for operation in work_order.operations:
		job = job_map[operation.operation]
		job_time_log = finergy.new_doc("Job Card Time Log")
		job_time_log.from_time = start_date
		minutes = operation.get("time_in_mins")
		job_time_log.time_in_mins = random.randint(int(minutes / 2), minutes)
		job_time_log.to_time = job_time_log.from_time + timedelta(minutes=job_time_log.time_in_mins)
		job_time_log.parent = job.name
		job_time_log.parenttype = "Job Card"
		job_time_log.parentfield = "time_logs"
		job_time_log.completed_qty = work_order.qty
		job_time_log.save(ignore_permissions=True)
		job.time_logs.append(job_time_log)
		job.save(ignore_permissions=True)
		job.submit()
		start_date = job_time_log.to_time
