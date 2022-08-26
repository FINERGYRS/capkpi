# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class MembershipType(Document):
	def validate(self):
		if self.linked_item:
			is_stock_item = finergy.db.get_value("Item", self.linked_item, "is_stock_item")
			if is_stock_item:
				finergy.throw(_("The Linked Item should be a service item"))


def get_membership_type(razorpay_id):
	return finergy.db.exists("Membership Type", {"razorpay_plan_id": razorpay_id})
