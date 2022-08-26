import finergy
from finergy.model.utils.rename_field import rename_field


def execute():
	finergy.reload_doc("stock", "doctype", "item")
	finergy.reload_doc("stock", "doctype", "stock_settings")
	finergy.reload_doc("accounts", "doctype", "accounts_settings")

	rename_field("Stock Settings", "tolerance", "over_delivery_receipt_allowance")
	rename_field("Item", "tolerance", "over_delivery_receipt_allowance")

	qty_allowance = finergy.db.get_single_value("Stock Settings", "over_delivery_receipt_allowance")
	finergy.db.set_value("Accounts Settings", None, "over_delivery_receipt_allowance", qty_allowance)

	finergy.db.sql("update tabItem set over_billing_allowance=over_delivery_receipt_allowance")
