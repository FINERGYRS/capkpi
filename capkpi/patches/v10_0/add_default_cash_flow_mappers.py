# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

from capkpi.setup.install import create_default_cash_flow_mapper_templates


def execute():
	finergy.reload_doc("accounts", "doctype", finergy.scrub("Cash Flow Mapping"))
	finergy.reload_doc("accounts", "doctype", finergy.scrub("Cash Flow Mapper"))
	finergy.reload_doc("accounts", "doctype", finergy.scrub("Cash Flow Mapping Template Details"))

	create_default_cash_flow_mapper_templates()
