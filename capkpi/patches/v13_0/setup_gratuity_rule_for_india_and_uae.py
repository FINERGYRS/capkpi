# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("payroll", "doctype", "gratuity_rule")
	finergy.reload_doc("payroll", "doctype", "gratuity_rule_slab")
	finergy.reload_doc("payroll", "doctype", "gratuity_applicable_component")
	if finergy.db.exists("Company", {"country": "India"}):
		from capkpi.regional.india.setup import create_gratuity_rule

		create_gratuity_rule()
	if finergy.db.exists("Company", {"country": "United Arab Emirates"}):
		from capkpi.regional.united_arab_emirates.setup import create_gratuity_rule

		create_gratuity_rule()
