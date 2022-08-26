import finergy


def pre_process(issue):

	project = finergy.db.get_value("Project", filters={"project_name": issue.milestone})
	return {
		"title": issue.title,
		"body": finergy.utils.md_to_html(issue.body or ""),
		"state": issue.state.title(),
		"project": project or "",
	}
