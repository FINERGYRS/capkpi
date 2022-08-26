# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class ProjectType(Document):
	def on_trash(self):
		if self.name == "External":
			finergy.throw(_("You cannot delete Project Type 'External'"))
