import finergy


def execute():
	for dt, dn in (("Page", "Hub"), ("DocType", "Hub Settings"), ("DocType", "Hub Category")):
		finergy.delete_doc(dt, dn, ignore_missing=True)

	if finergy.db.exists("DocType", "Data Migration Plan"):
		data_migration_plans = finergy.get_all("Data Migration Plan", filters={"module": "Hub Node"})
		for plan in data_migration_plans:
			plan_doc = finergy.get_doc("Data Migration Plan", plan.name)
			for m in plan_doc.get("mappings"):
				finergy.delete_doc("Data Migration Mapping", m.mapping, force=True)
			docs = finergy.get_all("Data Migration Run", filters={"data_migration_plan": plan.name})
			for doc in docs:
				finergy.delete_doc("Data Migration Run", doc.name)
			finergy.delete_doc("Data Migration Plan", plan.name)
