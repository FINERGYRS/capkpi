import finergy
from finergy.model.utils.rename_field import rename_field


def execute():
	finergy.reload_doc("Healthcare", "doctype", "Inpatient Record")
	if finergy.db.has_column("Inpatient Record", "discharge_date"):
		rename_field("Inpatient Record", "discharge_date", "discharge_datetime")
