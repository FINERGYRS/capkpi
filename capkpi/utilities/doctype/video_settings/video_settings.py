# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from apiclient.discovery import build
from finergy import _
from finergy.model.document import Document


class VideoSettings(Document):
	def validate(self):
		self.validate_youtube_api_key()

	def validate_youtube_api_key(self):
		if self.enable_youtube_tracking and self.api_key:
			try:
				build("youtube", "v3", developerKey=self.api_key)
			except Exception:
				title = _("Failed to Authenticate the API key.")
				self.log_error("Failed to authenticate API key")
				finergy.throw(title + " Please check the error logs.", title=_("Invalid Credentials"))
