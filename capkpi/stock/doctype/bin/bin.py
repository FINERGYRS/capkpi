# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.model.document import Document
from finergy.query_builder import Case, Order
from finergy.query_builder.functions import Coalesce, CombineDatetime, Sum
from finergy.utils import flt


class Bin(Document):
	def before_save(self):
		if self.get("__islocal") or not self.stock_uom:
			self.stock_uom = finergy.get_cached_value("Item", self.item_code, "stock_uom")
		self.set_projected_qty()

	def set_projected_qty(self):
		self.projected_qty = (
			flt(self.actual_qty)
			+ flt(self.ordered_qty)
			+ flt(self.indented_qty)
			+ flt(self.planned_qty)
			- flt(self.reserved_qty)
			- flt(self.reserved_qty_for_production)
			- flt(self.reserved_qty_for_sub_contract)
		)

	def update_reserved_qty_for_production(self):
		"""Update qty reserved for production from Production Item tables
		in open work orders"""
		from capkpi.manufacturing.doctype.work_order.work_order import get_reserved_qty_for_production

		self.reserved_qty_for_production = get_reserved_qty_for_production(
			self.item_code, self.warehouse
		)

		self.set_projected_qty()

		self.db_set("reserved_qty_for_production", flt(self.reserved_qty_for_production))
		self.db_set("projected_qty", self.projected_qty)

	def update_reserved_qty_for_sub_contracting(self, subcontract_doctype="Subcontracting Order"):
		# reserved qty

		subcontract_order = finergy.qb.DocType(subcontract_doctype)
		supplied_item = finergy.qb.DocType(
			"Purchase Order Item Supplied"
			if subcontract_doctype == "Purchase Order"
			else "Subcontracting Order Supplied Item"
		)

		conditions = (
			(supplied_item.rm_item_code == self.item_code)
			& (subcontract_order.name == supplied_item.parent)
			& (subcontract_order.per_received < 100)
			& (supplied_item.reserve_warehouse == self.warehouse)
			& (
				(
					(subcontract_order.is_old_subcontracting_flow == 1)
					& (subcontract_order.status != "Closed")
					& (subcontract_order.docstatus == 1)
				)
				if subcontract_doctype == "Purchase Order"
				else (subcontract_order.docstatus == 1)
			)
		)

		reserved_qty_for_sub_contract = (
			finergy.qb.from_(subcontract_order)
			.from_(supplied_item)
			.select(Sum(Coalesce(supplied_item.required_qty, 0)))
			.where(conditions)
		).run()[0][0] or 0.0

		se = finergy.qb.DocType("Stock Entry")
		se_item = finergy.qb.DocType("Stock Entry Detail")

		if finergy.db.field_exists("Stock Entry", "is_return"):
			qty_field = (
				Case().when(se.is_return == 1, se_item.transfer_qty * -1).else_(se_item.transfer_qty)
			)
		else:
			qty_field = se_item.transfer_qty

		conditions = (
			(se.docstatus == 1)
			& (se.purpose == "Send to Subcontractor")
			& ((se_item.item_code == self.item_code) | (se_item.original_item == self.item_code))
			& (se.name == se_item.parent)
			& (subcontract_order.docstatus == 1)
			& (subcontract_order.per_received < 100)
			& (
				(
					(Coalesce(se.purchase_order, "") != "")
					& (subcontract_order.name == se.purchase_order)
					& (subcontract_order.is_old_subcontracting_flow == 1)
					& (subcontract_order.status != "Closed")
				)
				if subcontract_doctype == "Purchase Order"
				else (
					(Coalesce(se.subcontracting_order, "") != "")
					& (subcontract_order.name == se.subcontracting_order)
				)
			)
		)

		materials_transferred = (
			finergy.qb.from_(se)
			.from_(se_item)
			.from_(subcontract_order)
			.select(Sum(qty_field))
			.where(conditions)
		).run()[0][0] or 0.0

		if reserved_qty_for_sub_contract > materials_transferred:
			reserved_qty_for_sub_contract = reserved_qty_for_sub_contract - materials_transferred
		else:
			reserved_qty_for_sub_contract = 0

		self.db_set("reserved_qty_for_sub_contract", reserved_qty_for_sub_contract)
		self.set_projected_qty()
		self.db_set("projected_qty", self.projected_qty)


def on_doctype_update():
	finergy.db.add_unique("Bin", ["item_code", "warehouse"], constraint_name="unique_item_warehouse")


def get_bin_details(bin_name):
	return finergy.db.get_value(
		"Bin",
		bin_name,
		[
			"actual_qty",
			"ordered_qty",
			"reserved_qty",
			"indented_qty",
			"planned_qty",
			"reserved_qty_for_production",
			"reserved_qty_for_sub_contract",
		],
		as_dict=1,
	)


def update_qty(bin_name, args):
	from capkpi.controllers.stock_controller import future_sle_exists

	bin_details = get_bin_details(bin_name)
	# actual qty is already updated by processing current voucher
	actual_qty = bin_details.actual_qty or 0.0
	sle = finergy.qb.DocType("Stock Ledger Entry")

	# actual qty is not up to date in case of backdated transaction
	if future_sle_exists(args):
		last_sle_qty = (
			finergy.qb.from_(sle)
			.select(sle.qty_after_transaction)
			.where((sle.item_code == args.get("item_code")) & (sle.warehouse == args.get("warehouse")))
			.orderby(CombineDatetime(sle.posting_date, sle.posting_time), order=Order.desc)
			.orderby(sle.creation, order=Order.desc)
			.run()
		)

		if last_sle_qty:
			actual_qty = last_sle_qty[0][0]

	ordered_qty = flt(bin_details.ordered_qty) + flt(args.get("ordered_qty"))
	reserved_qty = flt(bin_details.reserved_qty) + flt(args.get("reserved_qty"))
	indented_qty = flt(bin_details.indented_qty) + flt(args.get("indented_qty"))
	planned_qty = flt(bin_details.planned_qty) + flt(args.get("planned_qty"))

	# compute projected qty
	projected_qty = (
		flt(actual_qty)
		+ flt(ordered_qty)
		+ flt(indented_qty)
		+ flt(planned_qty)
		- flt(reserved_qty)
		- flt(bin_details.reserved_qty_for_production)
		- flt(bin_details.reserved_qty_for_sub_contract)
	)

	finergy.db.set_value(
		"Bin",
		bin_name,
		{
			"actual_qty": actual_qty,
			"ordered_qty": ordered_qty,
			"reserved_qty": reserved_qty,
			"indented_qty": indented_qty,
			"planned_qty": planned_qty,
			"projected_qty": projected_qty,
		},
	)
