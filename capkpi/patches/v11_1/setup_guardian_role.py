import finergy


def execute():
	if "Education" in finergy.get_active_domains() and not finergy.db.exists("Role", "Guardian"):
		doc = finergy.new_doc("Role")
		doc.update({"role_name": "Guardian", "desk_access": 0})

		doc.insert(ignore_permissions=True)
