# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy import _
from finergy.model.document import Document


class Topic(Document):
	def get_contents(self):
		try:
			topic_content_list = self.topic_content
			content_data = [
				finergy.get_doc(topic_content.content_type, topic_content.content)
				for topic_content in topic_content_list
			]
		except Exception as e:
			finergy.log_error(finergy.get_traceback())
			return None
		return content_data


@finergy.whitelist()
def get_courses_without_topic(topic):
	data = []
	for entry in finergy.db.get_all("Course"):
		course = finergy.get_doc("Course", entry.name)
		topics = [t.topic for t in course.topics]
		if not topics or topic not in topics:
			data.append(course.name)
	return data


@finergy.whitelist()
def add_topic_to_courses(topic, courses, mandatory=False):
	courses = json.loads(courses)
	for entry in courses:
		course = finergy.get_doc("Course", entry)
		course.append("topics", {"topic": topic, "topic_name": topic})
		course.flags.ignore_mandatory = True
		course.save()
	finergy.db.commit()
	finergy.msgprint(
		_("Topic {0} has been added to all the selected courses successfully.").format(
			finergy.bold(topic)
		),
		title=_("Courses updated"),
		indicator="green",
	)


@finergy.whitelist()
def add_content_to_topics(content_type, content, topics):
	topics = json.loads(topics)
	for entry in topics:
		topic = finergy.get_doc("Topic", entry)
		topic.append(
			"topic_content",
			{
				"content_type": content_type,
				"content": content,
			},
		)
		topic.flags.ignore_mandatory = True
		topic.save()
	finergy.db.commit()
	finergy.msgprint(
		_("{0} {1} has been added to all the selected topics successfully.").format(
			content_type, finergy.bold(content)
		),
		title=_("Topics updated"),
		indicator="green",
	)
