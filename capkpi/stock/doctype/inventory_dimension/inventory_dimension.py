# Copyright (c) 2022, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy import _, bold, scrub
from finergy.custom.doctype.custom_field.custom_field import create_custom_fields
from finergy.model.document import Document


class DoNotChangeError(finergy.ValidationError):
	pass


class CanNotBeChildDoc(finergy.ValidationError):
	pass


class CanNotBeDefaultDimension(finergy.ValidationError):
	pass


class InventoryDimension(Document):
	def onload(self):
		if not self.is_new() and finergy.db.has_column("Stock Ledger Entry", self.target_fieldname):
			self.set_onload("has_stock_ledger", self.has_stock_ledger())

	def has_stock_ledger(self) -> str:
		if not self.target_fieldname:
			return

		return finergy.get_all(
			"Stock Ledger Entry", filters={self.target_fieldname: ("is", "set"), "is_cancelled": 0}, limit=1
		)

	def validate(self):
		self.do_not_update_document()
		self.reset_value()
		self.validate_reference_document()
		self.set_source_and_target_fieldname()

	def do_not_update_document(self):
		if self.is_new() or not self.has_stock_ledger():
			return

		old_doc = self._doc_before_save
		allow_to_edit_fields = [
			"disabled",
			"fetch_from_parent",
			"type_of_transaction",
			"condition",
		]

		for field in finergy.get_meta("Inventory Dimension").fields:
			if field.fieldname not in allow_to_edit_fields and old_doc.get(field.fieldname) != self.get(
				field.fieldname
			):
				msg = f"""The user can not change value of the field {bold(field.label)} because
					stock transactions exists against the dimension {bold(self.name)}."""

				finergy.throw(_(msg), DoNotChangeError)

	def on_trash(self):
		self.delete_custom_fields()

	def delete_custom_fields(self):
		filters = {"fieldname": self.source_fieldname}

		if self.document_type:
			filters["dt"] = self.document_type

		for field in finergy.get_all("Custom Field", filters=filters):
			finergy.delete_doc("Custom Field", field.name)

		msg = f"Deleted custom fields related to the dimension {self.name}"
		finergy.msgprint(_(msg))

	def reset_value(self):
		if self.apply_to_all_doctypes:
			self.istable = 0
			for field in ["document_type", "condition"]:
				self.set(field, None)

	def validate_reference_document(self):
		if finergy.get_cached_value("DocType", self.reference_document, "istable") == 1:
			msg = f"The reference document {self.reference_document} can not be child table."
			finergy.throw(_(msg), CanNotBeChildDoc)

		if self.reference_document in ["Batch", "Serial No", "Warehouse", "Item"]:
			msg = f"The reference document {self.reference_document} can not be an Inventory Dimension."
			finergy.throw(_(msg), CanNotBeDefaultDimension)

	def set_source_and_target_fieldname(self) -> None:
		if not self.source_fieldname:
			self.source_fieldname = scrub(self.dimension_name)

		if not self.target_fieldname:
			self.target_fieldname = scrub(self.reference_document)

	def on_update(self):
		self.add_custom_fields()

	def add_custom_fields(self):
		dimension_fields = [
			dict(
				fieldname="inventory_dimension",
				fieldtype="Section Break",
				insert_after="warehouse",
				label="Inventory Dimension",
				collapsible=1,
			),
			dict(
				fieldname=self.source_fieldname,
				fieldtype="Link",
				insert_after="inventory_dimension",
				options=self.reference_document,
				label=self.dimension_name,
			),
		]

		custom_fields = {}

		if self.apply_to_all_doctypes:
			for doctype in get_inventory_documents():
				custom_fields.setdefault(doctype[0], dimension_fields)
		else:
			custom_fields.setdefault(self.document_type, dimension_fields)

		if not finergy.db.get_value(
			"Custom Field", {"dt": "Stock Ledger Entry", "fieldname": self.target_fieldname}
		):
			dimension_field = dimension_fields[1]
			dimension_field["fieldname"] = self.target_fieldname
			custom_fields["Stock Ledger Entry"] = dimension_field

		create_custom_fields(custom_fields)


@finergy.whitelist()
def get_inventory_documents(
	doctype=None, txt=None, searchfield=None, start=None, page_len=None, filters=None
):
	and_filters = [["DocField", "parent", "not in", ["Batch", "Serial No"]]]
	or_filters = [
		["DocField", "options", "in", ["Batch", "Serial No"]],
		["DocField", "parent", "in", ["Putaway Rule"]],
	]

	if txt:
		and_filters.append(["DocField", "parent", "like", f"%{txt}%"])

	return finergy.get_all(
		"DocField",
		fields=["distinct parent"],
		filters=and_filters,
		or_filters=or_filters,
		start=start,
		page_length=page_len,
		as_list=1,
	)


def get_evaluated_inventory_dimension(doc, sl_dict, parent_doc=None):
	dimensions = get_document_wise_inventory_dimensions(doc.doctype)
	filter_dimensions = []
	for row in dimensions:
		if (
			row.type_of_transaction == "Inward"
			if doc.docstatus == 1
			else row.type_of_transaction != "Inward"
		) and sl_dict.actual_qty < 0:
			continue
		elif (
			row.type_of_transaction == "Outward"
			if doc.docstatus == 1
			else row.type_of_transaction != "Outward"
		) and sl_dict.actual_qty > 0:
			continue

		evals = {"doc": doc}
		if parent_doc:
			evals["parent"] = parent_doc

		if row.condition and finergy.safe_eval(row.condition, evals):
			filter_dimensions.append(row)
		else:
			filter_dimensions.append(row)

	return filter_dimensions


def get_document_wise_inventory_dimensions(doctype) -> dict:
	if not hasattr(finergy.local, "document_wise_inventory_dimensions"):
		finergy.local.document_wise_inventory_dimensions = {}

	if not finergy.local.document_wise_inventory_dimensions.get(doctype):
		dimensions = finergy.get_all(
			"Inventory Dimension",
			fields=[
				"name",
				"source_fieldname",
				"condition",
				"target_fieldname",
				"type_of_transaction",
				"fetch_from_parent",
			],
			filters={"disabled": 0},
			or_filters={"document_type": doctype, "apply_to_all_doctypes": 1},
		)

		finergy.local.document_wise_inventory_dimensions[doctype] = dimensions

	return finergy.local.document_wise_inventory_dimensions[doctype]


@finergy.whitelist()
def get_inventory_dimensions():
	if not hasattr(finergy.local, "inventory_dimensions"):
		finergy.local.inventory_dimensions = {}

	if not finergy.local.inventory_dimensions:
		dimensions = finergy.get_all(
			"Inventory Dimension",
			fields=[
				"distinct target_fieldname as fieldname",
				"reference_document as doctype",
			],
			filters={"disabled": 0},
		)

		finergy.local.inventory_dimensions = dimensions

	return finergy.local.inventory_dimensions


@finergy.whitelist()
def delete_dimension(dimension):
	doc = finergy.get_doc("Inventory Dimension", dimension)
	doc.delete()
