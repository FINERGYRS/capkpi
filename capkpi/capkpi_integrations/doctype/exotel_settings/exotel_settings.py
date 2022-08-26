# Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
import requests
from finergy import _
from finergy.model.document import Document


class ExotelSettings(Document):
	def validate(self):
		self.verify_credentials()

	def verify_credentials(self):
		if self.enabled:
			response = requests.get(
				"https://api.exotel.com/v1/Accounts/{sid}".format(sid=self.account_sid),
				auth=(self.api_key, self.api_token),
			)
			if response.status_code != 200:
				finergy.throw(_("Invalid credentials"))
