import finergy


def execute():
	if finergy.db.has_column("Item", "thumbnail"):
		website_item = finergy.qb.DocType("Website Item").as_("wi")
		item = finergy.qb.DocType("Item")

		finergy.qb.update(website_item).inner_join(item).on(website_item.item_code == item.item_code).set(
			website_item.thumbnail, item.thumbnail
		).where(website_item.website_image.notnull() & website_item.thumbnail.isnull()).run()
