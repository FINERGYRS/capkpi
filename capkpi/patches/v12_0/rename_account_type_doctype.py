import finergy


def execute():
	finergy.rename_doc("DocType", "Account Type", "Bank Account Type", force=True)
	finergy.rename_doc("DocType", "Account Subtype", "Bank Account Subtype", force=True)
	finergy.reload_doc("accounts", "doctype", "bank_account")
