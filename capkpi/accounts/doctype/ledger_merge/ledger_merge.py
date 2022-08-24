# Copyright (c) 2021, Wahni Green Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import finergy
from finergy import _
from finergy.model.document import Document

from capkpi.accounts.doctype.account.account import merge_account


class LedgerMerge(Document):
	def start_merge(self):
		from finergy.core.page.background_jobs.background_jobs import get_info
		from finergy.utils.background_jobs import enqueue
		from finergy.utils.scheduler import is_scheduler_inactive

		if is_scheduler_inactive() and not finergy.flags.in_test:
			finergy.throw(_("Scheduler is inactive. Cannot merge accounts."), title=_("Scheduler Inactive"))

		enqueued_jobs = [d.get("job_name") for d in get_info()]

		if self.name not in enqueued_jobs:
			enqueue(
				start_merge,
				queue="default",
				timeout=6000,
				event="ledger_merge",
				job_name=self.name,
				docname=self.name,
				now=finergy.conf.developer_mode or finergy.flags.in_test,
			)
			return True

		return False


@finergy.whitelist()
def form_start_merge(docname):
	return finergy.get_doc("Ledger Merge", docname).start_merge()


def start_merge(docname):
	ledger_merge = finergy.get_doc("Ledger Merge", docname)
	successful_merges = 0
	total = len(ledger_merge.merge_accounts)
	for row in ledger_merge.merge_accounts:
		if not row.merged:
			try:
				merge_account(
					row.account,
					ledger_merge.account,
					ledger_merge.is_group,
					ledger_merge.root_type,
					ledger_merge.company,
				)
				row.db_set("merged", 1)
				finergy.db.commit()
				successful_merges += 1
				finergy.publish_realtime(
					"ledger_merge_progress",
					{"ledger_merge": ledger_merge.name, "current": successful_merges, "total": total},
				)
			except Exception:
				finergy.db.rollback()
				ledger_merge.log_error("Ledger merge failed")
			finally:
				if successful_merges == total:
					ledger_merge.db_set("status", "Success")
				elif successful_merges > 0:
					ledger_merge.db_set("status", "Partial Success")
				else:
					ledger_merge.db_set("status", "Error")

	finergy.publish_realtime("ledger_merge_refresh", {"ledger_merge": ledger_merge.name})
