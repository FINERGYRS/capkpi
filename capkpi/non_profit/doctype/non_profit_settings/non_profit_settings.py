# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.integrations.utils import get_payment_gateway_controller
from finergy.model.document import Document


class NonProfitSettings(Document):
	@finergy.whitelist()
	def generate_webhook_secret(self, field="membership_webhook_secret"):
		key = finergy.generate_hash(length=20)
		self.set(field, key)
		self.save()

		secret_for = "Membership" if field == "membership_webhook_secret" else "Donation"

		finergy.msgprint(
			_("Here is your webhook secret for {0} API, this will be shown to you only once.").format(
				secret_for
			)
			+ "<br><br>"
			+ key,
			_("Webhook Secret"),
		)

	@finergy.whitelist()
	def revoke_key(self, key):
		self.set(key, None)
		self.save()

	def get_webhook_secret(self, endpoint="Membership"):
		fieldname = (
			"membership_webhook_secret" if endpoint == "Membership" else "donation_webhook_secret"
		)
		return self.get_password(fieldname=fieldname, raise_exception=False)


@finergy.whitelist()
def get_plans_for_membership(*args, **kwargs):
	controller = get_payment_gateway_controller("Razorpay")
	plans = controller.get_plans()
	return [plan.get("item") for plan in plans.get("items")]
