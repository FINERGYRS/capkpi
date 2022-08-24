import finergy


def get_context(context):
	context.no_cache = 1

	task = finergy.get_doc("Task", finergy.form_dict.task)

	context.comments = finergy.get_all(
		"Communication",
		filters={"reference_name": task.name, "comment_type": "comment"},
		fields=["subject", "sender_full_name", "communication_date"],
	)

	context.doc = task
