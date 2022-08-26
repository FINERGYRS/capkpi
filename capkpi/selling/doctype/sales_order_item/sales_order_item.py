# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.model.document import Document


class SalesOrderItem(Document):
	pass


def on_doctype_update():
	finergy.db.add_index("Sales Order Item", ["item_code", "warehouse"])
