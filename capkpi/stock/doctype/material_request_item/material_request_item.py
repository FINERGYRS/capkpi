# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class MaterialRequestItem(Document):
	pass


def on_doctype_update():
	finergy.db.add_index("Material Request Item", ["item_code", "warehouse"])
