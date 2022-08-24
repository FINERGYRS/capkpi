# Copyright (c) 2020, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.model.utils.rename_field import rename_field


def execute():
	finergy.reload_doc("support", "doctype", "sla_fulfilled_on_status")
	finergy.reload_doc("support", "doctype", "service_level_agreement")
	if finergy.db.has_column("Service Level Agreement", "enable"):
		rename_field("Service Level Agreement", "enable", "enabled")

	for sla in finergy.get_all("Service Level Agreement"):
		agreement = finergy.get_doc("Service Level Agreement", sla.name)
		agreement.document_type = "Issue"
		agreement.apply_sla_for_resolution = 1
		agreement.append("sla_fulfilled_on", {"status": "Resolved"})
		agreement.append("sla_fulfilled_on", {"status": "Closed"})
		agreement.save()
