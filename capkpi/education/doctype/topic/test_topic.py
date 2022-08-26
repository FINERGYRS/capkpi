# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy


class TestTopic(unittest.TestCase):
	def setUp(self):
		make_topic_and_linked_content("_Test Topic 1", [{"type": "Article", "name": "_Test Article 1"}])

	def test_get_contents(self):
		topic = finergy.get_doc("Topic", "_Test Topic 1")
		contents = topic.get_contents()
		self.assertEqual(contents[0].doctype, "Article")
		self.assertEqual(contents[0].name, "_Test Article 1")
		finergy.db.rollback()


def make_topic(name):
	try:
		topic = finergy.get_doc("Topic", name)
	except finergy.DoesNotExistError:
		topic = finergy.get_doc(
			{
				"doctype": "Topic",
				"topic_name": name,
				"topic_code": name,
			}
		).insert()
	return topic.name


def make_topic_and_linked_content(topic_name, content_dict_list):
	try:
		topic = finergy.get_doc("Topic", topic_name)
	except finergy.DoesNotExistError:
		make_topic(topic_name)
		topic = finergy.get_doc("Topic", topic_name)
	content_list = [make_content(content["type"], content["name"]) for content in content_dict_list]
	for content in content_list:
		topic.append("topic_content", {"content": content.title, "content_type": content.doctype})
	topic.save()
	return topic


def make_content(type, name):
	try:
		content = finergy.get_doc(type, name)
	except finergy.DoesNotExistError:
		content = finergy.get_doc({"doctype": type, "title": name}).insert()
	return content
