import finergy


def execute():
	if finergy.db.table_exists("Offer Letter") and not finergy.db.table_exists("Job Offer"):
		finergy.rename_doc("DocType", "Offer Letter", "Job Offer", force=True)
		finergy.rename_doc("DocType", "Offer Letter Term", "Job Offer Term", force=True)
		finergy.reload_doc("hr", "doctype", "job_offer")
		finergy.reload_doc("hr", "doctype", "job_offer_term")
		finergy.delete_doc("Print Format", "Offer Letter")
