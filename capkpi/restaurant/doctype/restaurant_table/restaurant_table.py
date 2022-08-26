# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import re

from finergy.model.document import Document
from finergy.model.naming import make_autoname


class RestaurantTable(Document):
	def autoname(self):
		prefix = re.sub("-+", "-", self.restaurant.replace(" ", "-"))
		self.name = make_autoname(prefix + "-.##")
