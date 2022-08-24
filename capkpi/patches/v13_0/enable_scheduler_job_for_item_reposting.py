import finergy


def execute():
	finergy.reload_doc("core", "doctype", "scheduled_job_type")
	if finergy.db.exists("Scheduled Job Type", "repost_item_valuation.repost_entries"):
		finergy.db.set_value("Scheduled Job Type", "repost_item_valuation.repost_entries", "stopped", 0)
