import finergy


def execute():
	name = finergy.db.sql(
		""" select name from `tabPatch Log` \
		where \
			patch like 'execute:finergy.db.sql("update `tabProduction Order` pro set description%' """
	)
	if not name:
		finergy.db.sql(
			"update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''"
		)
