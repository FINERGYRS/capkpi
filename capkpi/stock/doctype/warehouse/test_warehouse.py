# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import finergy
from finergy.test_runner import make_test_records
from finergy.tests.utils import FinergyTestCase

import capkpi
from capkpi.accounts.doctype.account.test_account import create_account
from capkpi.stock.doctype.item.test_item import create_item
from capkpi.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from capkpi.stock.doctype.warehouse.warehouse import convert_to_group_or_ledger, get_children

test_records = finergy.get_test_records("Warehouse")


class TestWarehouse(FinergyTestCase):
	def setUp(self):
		super().setUp()
		if not finergy.get_value("Item", "_Test Item"):
			make_test_records("Item")

	def test_parent_warehouse(self):
		parent_warehouse = finergy.get_doc("Warehouse", "_Test Warehouse Group - _TC")
		self.assertEqual(parent_warehouse.is_group, 1)

	def test_warehouse_hierarchy(self):
		p_warehouse = finergy.get_doc("Warehouse", "_Test Warehouse Group - _TC")

		child_warehouses = finergy.db.sql(
			"""select name, is_group, parent_warehouse from `tabWarehouse` wh
			where wh.lft > %s and wh.rgt < %s""",
			(p_warehouse.lft, p_warehouse.rgt),
			as_dict=1,
		)

		for child_warehouse in child_warehouses:
			self.assertEqual(p_warehouse.name, child_warehouse.parent_warehouse)
			self.assertEqual(child_warehouse.is_group, 0)

	def test_naming(self):
		company = "Wind Power LLC"
		warehouse_name = "Named Warehouse - WP"
		wh = finergy.get_doc(doctype="Warehouse", warehouse_name=warehouse_name, company=company).insert()
		self.assertEqual(wh.name, warehouse_name)

		warehouse_name = "Unnamed Warehouse"
		wh = finergy.get_doc(doctype="Warehouse", warehouse_name=warehouse_name, company=company).insert()
		self.assertIn(warehouse_name, wh.name)

	def test_unlinking_warehouse_from_item_defaults(self):
		company = "_Test Company"

		warehouse_names = [f"_Test Warehouse {i} for Unlinking" for i in range(2)]
		warehouse_ids = []
		for warehouse in warehouse_names:
			warehouse_id = create_warehouse(warehouse, company=company)
			warehouse_ids.append(warehouse_id)

		item_names = [f"_Test Item {i} for Unlinking" for i in range(2)]
		for item, warehouse in zip(item_names, warehouse_ids):
			create_item(item, warehouse=warehouse, company=company)

		# Delete warehouses
		for warehouse in warehouse_ids:
			finergy.delete_doc("Warehouse", warehouse)

		# Check Item existance
		for item in item_names:
			self.assertTrue(bool(finergy.db.exists("Item", item)), f"{item} doesn't exist")

			item_doc = finergy.get_doc("Item", item)
			for item_default in item_doc.item_defaults:
				self.assertNotIn(
					item_default.default_warehouse,
					warehouse_ids,
					f"{item} linked to {item_default.default_warehouse} in {warehouse_ids}.",
				)

	def test_group_non_group_conversion(self):

		warehouse = finergy.get_doc("Warehouse", create_warehouse("TestGroupConversion"))

		convert_to_group_or_ledger(warehouse.name)
		warehouse.reload()
		self.assertEqual(warehouse.is_group, 1)

		child = create_warehouse("GroupWHChild", {"parent_warehouse": warehouse.name})
		# chid exists
		self.assertRaises(finergy.ValidationError, convert_to_group_or_ledger, warehouse.name)
		finergy.delete_doc("Warehouse", child)

		convert_to_group_or_ledger(warehouse.name)
		warehouse.reload()
		self.assertEqual(warehouse.is_group, 0)

		make_stock_entry(item_code="_Test Item", target=warehouse.name, qty=1)
		# SLE exists
		self.assertRaises(finergy.ValidationError, convert_to_group_or_ledger, warehouse.name)

	def test_get_children(self):
		company = "_Test Company"

		children = get_children("Warehouse", parent=company, company=company, is_root=True)
		self.assertTrue(any(wh["value"] == "_Test Warehouse - _TC" for wh in children))


def create_warehouse(warehouse_name, properties=None, company=None):
	if not company:
		company = "_Test Company"

	warehouse_id = capkpi.encode_company_abbr(warehouse_name, company)
	if not finergy.db.exists("Warehouse", warehouse_id):
		w = finergy.new_doc("Warehouse")
		w.warehouse_name = warehouse_name
		w.parent_warehouse = "_Test Warehouse Group - _TC"
		w.company = company
		w.account = get_warehouse_account(warehouse_name, company)
		if properties:
			w.update(properties)
		w.save()
		return w.name
	else:
		return warehouse_id


def get_warehouse(**args):
	args = finergy._dict(args)
	if finergy.db.exists("Warehouse", args.warehouse_name + " - " + args.abbr):
		return finergy.get_doc("Warehouse", args.warehouse_name + " - " + args.abbr)
	else:
		w = finergy.get_doc(
			{
				"company": args.company or "_Test Company",
				"doctype": "Warehouse",
				"warehouse_name": args.warehouse_name,
				"is_group": 0,
				"account": get_warehouse_account(args.warehouse_name, args.company, args.abbr),
			}
		)
		w.insert()
		return w


def get_warehouse_account(warehouse_name, company, company_abbr=None):
	if not company_abbr:
		company_abbr = finergy.get_cached_value("Company", company, "abbr")

	if not finergy.db.exists("Account", warehouse_name + " - " + company_abbr):
		return create_account(
			account_name=warehouse_name,
			parent_account=get_group_stock_account(company, company_abbr),
			account_type="Stock",
			company=company,
		)
	else:
		return warehouse_name + " - " + company_abbr


def get_group_stock_account(company, company_abbr=None):
	group_stock_account = finergy.db.get_value(
		"Account", filters={"account_type": "Stock", "is_group": 1, "company": company}, fieldname="name"
	)
	if not group_stock_account:
		if not company_abbr:
			company_abbr = finergy.get_cached_value("Company", company, "abbr")
		group_stock_account = "Current Assets - " + company_abbr
	return group_stock_account
