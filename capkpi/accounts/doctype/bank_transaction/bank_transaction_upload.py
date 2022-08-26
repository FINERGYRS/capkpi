# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy.utils import getdate
from finergy.utils.dateutils import parse_date
from six import iteritems


@finergy.whitelist()
def upload_bank_statement():
	if getattr(finergy, "uploaded_file", None):
		with open(finergy.uploaded_file, "rb") as upfile:
			fcontent = upfile.read()
	else:
		fcontent = finergy.local.uploaded_file
		fname = finergy.local.uploaded_filename

	if finergy.safe_encode(fname).lower().endswith("csv".encode("utf-8")):
		from finergy.utils.csvutils import read_csv_content

		rows = read_csv_content(fcontent, False)

	elif finergy.safe_encode(fname).lower().endswith("xlsx".encode("utf-8")):
		from finergy.utils.xlsxutils import read_xlsx_file_from_attached_file

		rows = read_xlsx_file_from_attached_file(fcontent=fcontent)

	columns = rows[0]
	rows.pop(0)
	data = rows
	return {"columns": columns, "data": data}


@finergy.whitelist()
def create_bank_entries(columns, data, bank_account):
	header_map = get_header_mapping(columns, bank_account)

	success = 0
	errors = 0
	for d in json.loads(data):
		if all(item is None for item in d) is True:
			continue
		fields = {}
		for key, value in iteritems(header_map):
			fields.update({key: d[int(value) - 1]})

		try:
			bank_transaction = finergy.get_doc({"doctype": "Bank Transaction"})
			bank_transaction.update(fields)
			bank_transaction.date = getdate(parse_date(bank_transaction.date))
			bank_transaction.bank_account = bank_account
			bank_transaction.insert()
			bank_transaction.submit()
			success += 1
		except Exception:
			finergy.log_error(finergy.get_traceback())
			errors += 1

	return {"success": success, "errors": errors}


def get_header_mapping(columns, bank_account):
	mapping = get_bank_mapping(bank_account)

	header_map = {}
	for column in json.loads(columns):
		if column["content"] in mapping:
			header_map.update({mapping[column["content"]]: column["colIndex"]})

	return header_map


def get_bank_mapping(bank_account):
	bank_name = finergy.db.get_value("Bank Account", bank_account, "bank")
	bank = finergy.get_doc("Bank", bank_name)

	mapping = {row.file_field: row.bank_transaction_field for row in bank.bank_transaction_mapping}

	return mapping
