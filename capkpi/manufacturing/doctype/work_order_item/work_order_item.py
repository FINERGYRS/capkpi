# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class WorkOrderItem(Document):
	pass


def on_doctype_update():
	finergy.db.add_index("Work Order Item", ["item_code", "source_warehouse"])
