# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors and contributors
# For license information, please see license.txt


import finergy
from dateutil.relativedelta import relativedelta
from finergy.model.document import Document
from finergy.utils import cint


class ManufacturingSettings(Document):
	pass


def get_mins_between_operations():
	return relativedelta(
		minutes=cint(finergy.db.get_single_value("Manufacturing Settings", "mins_between_operations"))
		or 10
	)


@finergy.whitelist()
def is_material_consumption_enabled():
	if not hasattr(finergy.local, "material_consumption"):
		finergy.local.material_consumption = cint(
			finergy.db.get_single_value("Manufacturing Settings", "material_consumption")
		)

	return finergy.local.material_consumption
