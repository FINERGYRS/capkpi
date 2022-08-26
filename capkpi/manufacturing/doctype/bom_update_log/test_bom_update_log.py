# Copyright (c) 2022, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import finergy
from finergy.tests.utils import FinergyTestCase

from capkpi.manufacturing.doctype.bom_update_log.bom_update_log import (
	BOMMissingError,
	resume_bom_cost_update_jobs,
)
from capkpi.manufacturing.doctype.bom_update_tool.bom_update_tool import (
	enqueue_replace_bom,
	enqueue_update_cost,
)

test_records = finergy.get_test_records("BOM")


class TestBOMUpdateLog(FinergyTestCase):
	"Test BOM Update Tool Operations via BOM Update Log."

	def setUp(self):
		bom_doc = finergy.copy_doc(test_records[0])
		bom_doc.items[1].item_code = "_Test Item"
		bom_doc.insert()

		self.boms = finergy._dict(
			current_bom="BOM-_Test Item Home Desktop Manufactured-001",
			new_bom=bom_doc.name,
		)

		self.new_bom_doc = bom_doc

	def tearDown(self):
		finergy.db.rollback()

	def test_bom_update_log_validate(self):
		"""
		1) Test if BOM presence is validated.
		2) Test if same BOMs are validated.
		3) Test of non-existent BOM is validated.
		"""

		with self.assertRaises(BOMMissingError):
			enqueue_replace_bom(boms={})

		with self.assertRaises(finergy.ValidationError):
			enqueue_replace_bom(boms=finergy._dict(current_bom=self.boms.new_bom, new_bom=self.boms.new_bom))

		with self.assertRaises(finergy.ValidationError):
			enqueue_replace_bom(boms=finergy._dict(current_bom=self.boms.new_bom, new_bom="Dummy BOM"))

	def test_bom_update_log_completion(self):
		"Test if BOM Update Log handles job completion correctly."

		log = enqueue_replace_bom(boms=self.boms)
		log.reload()
		self.assertEqual(log.status, "Completed")


def update_cost_in_all_boms_in_test():
	"""
	Utility to run 'Update Cost' job in tests without Cron job until fully complete.
	"""
	log = enqueue_update_cost()  # create BOM Update Log

	while log.status != "Completed":
		resume_bom_cost_update_jobs()  # run cron job until complete
		log.reload()

	return log
