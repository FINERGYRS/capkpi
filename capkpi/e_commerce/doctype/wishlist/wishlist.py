# -*- coding: utf-8 -*-
# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy.model.document import Document


class Wishlist(Document):
	pass


@finergy.whitelist()
def add_to_wishlist(item_code):
	"""Insert Item into wishlist."""

	if finergy.db.exists("Wishlist Item", {"item_code": item_code, "parent": finergy.session.user}):
		return

	web_item_data = finergy.db.get_value(
		"Website Item",
		{"item_code": item_code},
		[
			"website_image",
			"website_warehouse",
			"name",
			"web_item_name",
			"item_name",
			"item_group",
			"route",
		],
		as_dict=1,
	)

	wished_item_dict = {
		"item_code": item_code,
		"item_name": web_item_data.get("item_name"),
		"item_group": web_item_data.get("item_group"),
		"website_item": web_item_data.get("name"),
		"web_item_name": web_item_data.get("web_item_name"),
		"image": web_item_data.get("website_image"),
		"warehouse": web_item_data.get("website_warehouse"),
		"route": web_item_data.get("route"),
	}

	if not finergy.db.exists("Wishlist", finergy.session.user):
		# initialise wishlist
		wishlist = finergy.get_doc({"doctype": "Wishlist"})
		wishlist.user = finergy.session.user
		wishlist.append("items", wished_item_dict)
		wishlist.save(ignore_permissions=True)
	else:
		wishlist = finergy.get_doc("Wishlist", finergy.session.user)
		item = wishlist.append("items", wished_item_dict)
		item.db_insert()

	if hasattr(finergy.local, "cookie_manager"):
		finergy.local.cookie_manager.set_cookie("wish_count", str(len(wishlist.items)))


@finergy.whitelist()
def remove_from_wishlist(item_code):
	if finergy.db.exists("Wishlist Item", {"item_code": item_code, "parent": finergy.session.user}):
		finergy.db.delete("Wishlist Item", {"item_code": item_code, "parent": finergy.session.user})
		finergy.db.commit()  # nosemgrep

		wishlist_items = finergy.db.get_values("Wishlist Item", filters={"parent": finergy.session.user})

		if hasattr(finergy.local, "cookie_manager"):
			finergy.local.cookie_manager.set_cookie("wish_count", str(len(wishlist_items)))
