import finergy


def get_context(context):
	context.no_cache = True
	chapter = finergy.get_doc("Chapter", finergy.form_dict.name)
	if finergy.session.user != "Guest":
		if finergy.session.user in [d.user for d in chapter.members if d.enabled == 1]:
			context.already_member = True
		else:
			if finergy.request.method == "GET":
				pass
			elif finergy.request.method == "POST":
				chapter.append(
					"members",
					dict(
						user=finergy.session.user,
						introduction=finergy.form_dict.introduction,
						website_url=finergy.form_dict.website_url,
						enabled=1,
					),
				)
				chapter.save(ignore_permissions=1)
				finergy.db.commit()

	context.chapter = chapter
