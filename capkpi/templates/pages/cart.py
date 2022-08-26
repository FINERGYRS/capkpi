# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

from capkpi.e_commerce.shopping_cart.cart import get_cart_quotation

no_cache = 1


def get_context(context):
	context.body_class = "product-page"
	context.update(get_cart_quotation())
