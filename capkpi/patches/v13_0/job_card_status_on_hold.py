import finergy


def execute():
	job_cards = finergy.get_all(
		"Job Card",
		{"status": "On Hold", "docstatus": ("!=", 0)},
		pluck="name",
	)

	for idx, job_card in enumerate(job_cards):
		try:
			doc = finergy.get_doc("Job Card", job_card)
			doc.set_status()
			doc.db_set("status", doc.status, update_modified=False)
			if idx % 100 == 0:
				finergy.db.commit()
		except Exception:
			continue
