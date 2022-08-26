import finergy


def get_context(context):
	context.no_cache = True
	chapter = finergy.get_doc("Chapter", finergy.form_dict.name)
	context.member_deleted = True
	context.chapter = chapter
