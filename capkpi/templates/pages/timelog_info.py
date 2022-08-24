import finergy


def get_context(context):
	context.no_cache = 1

	timelog = finergy.get_doc("Time Log", finergy.form_dict.timelog)

	context.doc = timelog
