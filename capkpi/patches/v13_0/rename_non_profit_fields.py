import finergy
from finergy.model.utils.rename_field import rename_field


def execute():
	if finergy.db.table_exists("Donation"):
		finergy.reload_doc("non_profit", "doctype", "Donation")

		rename_field("Donation", "razorpay_payment_id", "payment_id")

	if finergy.db.table_exists("Tax Exemption 80G Certificate"):
		finergy.reload_doc("regional", "doctype", "Tax Exemption 80G Certificate")
		finergy.reload_doc("regional", "doctype", "Tax Exemption 80G Certificate Detail")

		rename_field("Tax Exemption 80G Certificate", "razorpay_payment_id", "payment_id")
		rename_field("Tax Exemption 80G Certificate Detail", "razorpay_payment_id", "payment_id")
