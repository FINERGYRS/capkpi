# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document
from finergy.website.utils import delete_page_cache


class Homepage(Document):
	def validate(self):
		if not self.description:
			self.description = finergy._("This is an example website auto-generated from CapKPI")
		delete_page_cache("home")

	def setup_items(self):
		for d in finergy.get_all(
			"Website Item",
			fields=["name", "item_name", "description", "website_image", "route"],
			filters={"published": 1},
			limit=3,
		):

			doc = finergy.get_doc("Website Item", d.name)
			if not doc.route:
				# set missing route
				doc.save()
			self.append(
				"products",
				dict(
					item_code=d.name,
					item_name=d.item_name,
					description=d.description,
					image=d.website_image,
					route=d.route,
				),
			)
