# Copyright (c) 2019, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy

from capkpi.projects.doctype.task.test_task import create_task


class TestProjectTemplate(unittest.TestCase):
	pass


def make_project_template(project_template_name, project_tasks=[]):
	if not finergy.db.exists("Project Template", project_template_name):
		project_tasks = project_tasks or [
			create_task(subject="_Test Template Task 1", is_template=1, begin=0, duration=3),
			create_task(subject="_Test Template Task 2", is_template=1, begin=0, duration=2),
		]
		doc = finergy.get_doc(dict(doctype="Project Template", name=project_template_name))
		for task in project_tasks:
			doc.append("tasks", {"task": task.name})
		doc.insert()

	return finergy.get_doc("Project Template", project_template_name)
