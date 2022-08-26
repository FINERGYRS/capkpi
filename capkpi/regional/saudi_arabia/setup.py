# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import finergy
from finergy.permissions import add_permission, update_permission_property
from capkpi.regional.united_arab_emirates.setup import make_custom_fields as uae_custom_fields
from capkpi.regional.saudi_arabia.wizard.operations.setup_ksa_vat_setting import (
	create_ksa_vat_setting,
)
from finergy.custom.doctype.custom_field.custom_field import create_custom_fields


def setup(company=None, patch=True):
	uae_custom_fields()
	add_print_formats()
	add_permissions()
	make_custom_fields()


def add_print_formats():
	finergy.reload_doc("regional", "print_format", "detailed_tax_invoice", force=True)
	finergy.reload_doc("regional", "print_format", "simplified_tax_invoice", force=True)
	finergy.reload_doc("regional", "print_format", "tax_invoice", force=True)
	finergy.reload_doc("regional", "print_format", "ksa_vat_invoice", force=True)
	finergy.reload_doc("regional", "print_format", "ksa_pos_invoice", force=True)

	for d in (
		"Simplified Tax Invoice",
		"Detailed Tax Invoice",
		"Tax Invoice",
		"KSA VAT Invoice",
		"KSA POS Invoice",
	):
		finergy.db.set_value("Print Format", d, "disabled", 0)


def add_permissions():
	"""Add Permissions for KSA VAT Setting."""
	add_permission("KSA VAT Setting", "All", 0)
	for role in ("Accounts Manager", "Accounts User", "System Manager"):
		add_permission("KSA VAT Setting", role, 0)
		update_permission_property("KSA VAT Setting", role, 0, "write", 1)
		update_permission_property("KSA VAT Setting", role, 0, "create", 1)

	"""Enable KSA VAT Report"""
	finergy.db.set_value("Report", "KSA VAT", "disabled", 0)


def make_custom_fields():
	"""Create Custom fields
	- QR code Image file
	- Company Name in Arabic
	- Address in Arabic
	"""
	custom_fields = {
		"Sales Invoice": [
			dict(
				fieldname="ksa_einv_qr",
				label="KSA E-Invoicing QR",
				fieldtype="Attach Image",
				read_only=1,
				no_copy=1,
				hidden=1,
			)
		],
		"POS Invoice": [
			dict(
				fieldname="ksa_einv_qr",
				label="KSA E-Invoicing QR",
				fieldtype="Attach Image",
				read_only=1,
				no_copy=1,
				hidden=1,
			)
		],
		"Address": [
			dict(
				fieldname="address_in_arabic",
				label="Address in Arabic",
				fieldtype="Data",
				insert_after="address_line2",
			)
		],
		"Company": [
			dict(
				fieldname="company_name_in_arabic",
				label="Company Name In Arabic",
				fieldtype="Data",
				insert_after="company_name",
			)
		],
	}

	create_custom_fields(custom_fields, update=True)


def update_regional_tax_settings(country, company):
	create_ksa_vat_setting(company)
