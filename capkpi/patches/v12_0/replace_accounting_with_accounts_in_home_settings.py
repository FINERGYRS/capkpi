import finergy


def execute():
	finergy.db.sql(
		"""UPDATE `tabUser` SET `home_settings` = REPLACE(`home_settings`, 'Accounting', 'Accounts')"""
	)
	finergy.cache().delete_key("home_settings")
