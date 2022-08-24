import finergy


def execute():
	if finergy.db.exists("DocType", "Member"):
		finergy.reload_doc("Non Profit", "doctype", "Member")

		if finergy.db.has_column("Member", "subscription_activated"):
			finergy.db.sql(
				'UPDATE `tabMember` SET subscription_status = "Active" WHERE subscription_activated = 1'
			)
			finergy.db.sql_ddl("ALTER table `tabMember` DROP COLUMN subscription_activated")
