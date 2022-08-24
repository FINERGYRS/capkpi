# Copyright (c) 2021, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

no_cache = 1

from capkpi.e_commerce.shopping_cart.cart import get_cart_quotation


def get_context(context):
	context.body_class = "product-page"
	context.update(get_cart_quotation())
