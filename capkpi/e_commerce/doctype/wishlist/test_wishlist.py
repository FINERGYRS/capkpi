# -*- coding: utf-8 -*-
# Copyright (c) 2021, Finergy Reporting Solutions SAS and Contributors
# See license.txt
import unittest

import finergy
from finergy.core.doctype.user_permission.test_user_permission import create_user

from capkpi.e_commerce.doctype.website_item.website_item import make_website_item
from capkpi.e_commerce.doctype.wishlist.wishlist import add_to_wishlist, remove_from_wishlist
from capkpi.stock.doctype.item.test_item import make_item


class TestWishlist(unittest.TestCase):
	def setUp(self):
		item = make_item("Test Phone Series X")
		if not finergy.db.exists("Website Item", {"item_code": "Test Phone Series X"}):
			make_website_item(item, save=True)

		item = make_item("Test Phone Series Y")
		if not finergy.db.exists("Website Item", {"item_code": "Test Phone Series Y"}):
			make_website_item(item, save=True)

	def tearDown(self):
		finergy.get_cached_doc("Website Item", {"item_code": "Test Phone Series X"}).delete()
		finergy.get_cached_doc("Website Item", {"item_code": "Test Phone Series Y"}).delete()
		finergy.get_cached_doc("Item", "Test Phone Series X").delete()
		finergy.get_cached_doc("Item", "Test Phone Series Y").delete()

	def test_add_remove_items_in_wishlist(self):
		"Check if items are added and removed from user's wishlist."
		# add first item
		add_to_wishlist("Test Phone Series X")

		# check if wishlist was created and item was added
		self.assertTrue(finergy.db.exists("Wishlist", {"user": finergy.session.user}))
		self.assertTrue(
			finergy.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": finergy.session.user}
			)
		)

		# add second item to wishlist
		add_to_wishlist("Test Phone Series Y")
		wishlist_length = finergy.db.get_value(
			"Wishlist Item", {"parent": finergy.session.user}, "count(*)"
		)
		self.assertEqual(wishlist_length, 2)

		remove_from_wishlist("Test Phone Series X")
		remove_from_wishlist("Test Phone Series Y")

		wishlist_length = finergy.db.get_value(
			"Wishlist Item", {"parent": finergy.session.user}, "count(*)"
		)
		self.assertIsNone(finergy.db.exists("Wishlist Item", {"parent": finergy.session.user}))
		self.assertEqual(wishlist_length, 0)

		# tear down
		finergy.get_doc("Wishlist", {"user": finergy.session.user}).delete()

	def test_add_remove_in_wishlist_multiple_users(self):
		"Check if items are added and removed from the correct user's wishlist."
		test_user = create_user("test_reviewer@example.com", "Customer")
		test_user_1 = create_user("test_reviewer_1@example.com", "Customer")

		# add to wishlist for first user
		finergy.set_user(test_user.name)
		add_to_wishlist("Test Phone Series X")

		# add to wishlist for second user
		finergy.set_user(test_user_1.name)
		add_to_wishlist("Test Phone Series X")

		# check wishlist and its content for users
		self.assertTrue(finergy.db.exists("Wishlist", {"user": test_user.name}))
		self.assertTrue(
			finergy.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user.name}
			)
		)

		self.assertTrue(finergy.db.exists("Wishlist", {"user": test_user_1.name}))
		self.assertTrue(
			finergy.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user_1.name}
			)
		)

		# remove item for second user
		remove_from_wishlist("Test Phone Series X")

		# make sure item was removed for second user and not first
		self.assertFalse(
			finergy.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user_1.name}
			)
		)
		self.assertTrue(
			finergy.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user.name}
			)
		)

		# remove item for first user
		finergy.set_user(test_user.name)
		remove_from_wishlist("Test Phone Series X")
		self.assertFalse(
			finergy.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user.name}
			)
		)

		# tear down
		finergy.set_user("Administrator")
		finergy.get_doc("Wishlist", {"user": test_user.name}).delete()
		finergy.get_doc("Wishlist", {"user": test_user_1.name}).delete()
