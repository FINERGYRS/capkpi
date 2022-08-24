# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import copy

import finergy
from finergy.model.document import Document


class Brand(Document):
	pass


def get_brand_defaults(item, company):
	item = finergy.get_cached_doc("Item", item)
	if item.brand:
		brand = finergy.get_cached_doc("Brand", item.brand)

		for d in brand.brand_defaults or []:
			if d.company == company:
				row = copy.deepcopy(d.as_dict())
				row.pop("name")
				return row

	return finergy._dict()
