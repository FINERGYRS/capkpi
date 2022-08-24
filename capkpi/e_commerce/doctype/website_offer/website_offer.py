# -*- coding: utf-8 -*-
# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy.model.document import Document


class WebsiteOffer(Document):
	pass


@finergy.whitelist(allow_guest=True)
def get_offer_details(offer_id):
	return finergy.db.get_value("Website Offer", {"name": offer_id}, ["offer_details"])
