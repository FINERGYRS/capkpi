import finergy
from email_reply_parser import EmailReplyParser


@finergy.whitelist()
def get_data(start=0):
	# finergy.only_for('Employee', 'System Manager')
	data = finergy.get_all(
		"Communication",
		fields=("content", "text_content", "sender", "creation"),
		filters=dict(reference_doctype="Daily Work Summary"),
		order_by="creation desc",
		limit=40,
		start=start,
	)

	for d in data:
		d.sender_name = (
			finergy.db.get_value("Employee", {"user_id": d.sender}, "employee_name") or d.sender
		)
		if d.text_content:
			d.content = finergy.utils.md_to_html(EmailReplyParser.parse_reply(d.text_content))

	return data
