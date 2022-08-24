import finergy


def execute():
	"""Remove has_variants and attribute fields from item variant settings."""
	finergy.reload_doc("stock", "doctype", "Item Variant Settings")

	finergy.db.sql(
		"""delete from `tabVariant Field`
			where field_name in ('attributes', 'has_variants')"""
	)
