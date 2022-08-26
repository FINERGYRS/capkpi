import json

import finergy
from finergy import _
from finergy.desk.form.load import get_attachments
from finergy.finergyclient import FinergyClient
from six import string_types

current_user = finergy.session.user


@finergy.whitelist()
def register_marketplace(company, company_description):
	validate_registerer()

	settings = finergy.get_single("Marketplace Settings")
	message = settings.register_seller(company, company_description)

	if message.get("hub_seller_name"):
		settings.registered = 1
		settings.hub_seller_name = message.get("hub_seller_name")
		settings.save()

		settings.add_hub_user(finergy.session.user)

	return {"ok": 1}


@finergy.whitelist()
def register_users(user_list):
	user_list = json.loads(user_list)

	settings = finergy.get_single("Marketplace Settings")

	for user in user_list:
		settings.add_hub_user(user)

	return user_list


def validate_registerer():
	if current_user == "Administrator":
		finergy.throw(_("Please login as another user to register on Marketplace"))

	valid_roles = ["System Manager", "Item Manager"]

	if not finergy.utils.is_subset(valid_roles, finergy.get_roles()):
		finergy.throw(
			_("Only users with {0} role can register on Marketplace").format(", ".join(valid_roles)),
			finergy.PermissionError,
		)


@finergy.whitelist()
def call_hub_method(method, params=None):
	connection = get_hub_connection()

	if isinstance(params, string_types):
		params = json.loads(params)

	params.update({"cmd": "hub.hub.api." + method})

	response = connection.post_request(params)
	return response


def map_fields(items):
	field_mappings = get_field_mappings()
	table_fields = [d.fieldname for d in finergy.get_meta("Item").get_table_fields()]

	hub_seller_name = finergy.db.get_value(
		"Marketplace Settings", "Marketplace Settings", "hub_seller_name"
	)

	for item in items:
		for fieldname in table_fields:
			item.pop(fieldname, None)

		for mapping in field_mappings:
			local_fieldname = mapping.get("local_fieldname")
			remote_fieldname = mapping.get("remote_fieldname")

			value = item.get(local_fieldname)
			item.pop(local_fieldname, None)
			item[remote_fieldname] = value

		item["doctype"] = "Hub Item"
		item["hub_seller"] = hub_seller_name
		item.pop("attachments", None)

	return items


@finergy.whitelist()
def get_valid_items(search_value=""):
	items = finergy.get_list(
		"Item",
		fields=["*"],
		filters={"disabled": 0, "item_name": ["like", "%" + search_value + "%"], "publish_in_hub": 0},
		order_by="modified desc",
	)

	valid_items = filter(lambda x: x.image and x.description, items)

	def prepare_item(item):
		item.source_type = "local"
		item.attachments = get_attachments("Item", item.item_code)
		return item

	valid_items = map(prepare_item, valid_items)

	return valid_items


@finergy.whitelist()
def update_item(ref_doc, data):
	data = json.loads(data)

	data.update(dict(doctype="Hub Item", name=ref_doc))
	try:
		connection = get_hub_connection()
		connection.update(data)
	except Exception as e:
		finergy.log_error(message=e, title="Hub Sync Error")


@finergy.whitelist()
def publish_selected_items(items_to_publish):
	items_to_publish = json.loads(items_to_publish)
	items_to_update = []
	if not len(items_to_publish):
		finergy.throw(_("No items to publish"))

	for item in items_to_publish:
		item_code = item.get("item_code")
		finergy.db.set_value("Item", item_code, "publish_in_hub", 1)

		hub_dict = {
			"doctype": "Hub Tracked Item",
			"item_code": item_code,
			"published": 1,
			"hub_category": item.get("hub_category"),
			"image_list": item.get("image_list"),
		}
		finergy.get_doc(hub_dict).insert(ignore_if_duplicate=True)

	items = map_fields(items_to_publish)

	try:
		item_sync_preprocess(len(items))
		convert_relative_image_urls_to_absolute(items)

		# TODO: Publish Progress
		connection = get_hub_connection()
		connection.insert_many(items)

		item_sync_postprocess()
	except Exception as e:
		finergy.log_error(message=e, title="Hub Sync Error")


@finergy.whitelist()
def unpublish_item(item_code, hub_item_name):
	"""Remove item listing from the marketplace"""

	response = call_hub_method("unpublish_item", {"hub_item_name": hub_item_name})

	if response:
		finergy.db.set_value("Item", item_code, "publish_in_hub", 0)
		finergy.delete_doc("Hub Tracked Item", item_code)
	else:
		finergy.throw(_("Unable to update remote activity"))


@finergy.whitelist()
def get_unregistered_users():
	settings = finergy.get_single("Marketplace Settings")
	registered_users = [user.user for user in settings.users] + ["Administrator", "Guest"]
	all_users = [user.name for user in finergy.db.get_all("User", filters={"enabled": 1})]
	unregistered_users = [user for user in all_users if user not in registered_users]
	return unregistered_users


def item_sync_preprocess(intended_item_publish_count):
	response = call_hub_method(
		"pre_items_publish", {"intended_item_publish_count": intended_item_publish_count}
	)

	if response:
		finergy.db.set_value("Marketplace Settings", "Marketplace Settings", "sync_in_progress", 1)
		return response
	else:
		finergy.throw(_("Unable to update remote activity"))


def item_sync_postprocess():
	response = call_hub_method("post_items_publish", {})
	if response:
		finergy.db.set_value(
			"Marketplace Settings", "Marketplace Settings", "last_sync_datetime", finergy.utils.now()
		)
	else:
		finergy.throw(_("Unable to update remote activity"))

	finergy.db.set_value("Marketplace Settings", "Marketplace Settings", "sync_in_progress", 0)


def convert_relative_image_urls_to_absolute(items):
	from six.moves.urllib.parse import urljoin

	for item in items:
		file_path = item["image"]

		if file_path.startswith("/files/"):
			item["image"] = urljoin(finergy.utils.get_url(), file_path)


def get_hub_connection():
	settings = finergy.get_single("Marketplace Settings")
	marketplace_url = settings.marketplace_url
	hub_user = settings.get_hub_user(finergy.session.user)

	if hub_user:
		password = hub_user.get_password()
		hub_connection = FinergyClient(marketplace_url, hub_user.user, password)
		return hub_connection
	else:
		read_only_hub_connection = FinergyClient(marketplace_url)
		return read_only_hub_connection


def get_field_mappings():
	return []
