finergy.provide('capkpi.hub');

finergy.views.MarketplaceFactory = class MarketplaceFactory extends finergy.views.Factory {
	show() {
		is_marketplace_disabled()
			.then(disabled => {
				if (disabled) {
					finergy.show_not_found('Marketplace');
					return;
				}

				if (finergy.pages.marketplace) {
					finergy.container.change_to('marketplace');
					capkpi.hub.marketplace.refresh();
				} else {
					this.make('marketplace');
				}
			});
	}

	make(page_name) {
		const assets = [
			'/assets/js/marketplace.min.js'
		];

		finergy.require(assets, () => {
			capkpi.hub.marketplace = new capkpi.hub.Marketplace({
				parent: this.make_page(true, page_name)
			});
		});
	}
};

function is_marketplace_disabled() {
	return finergy.call({
		method: "capkpi.hub_node.doctype.marketplace_settings.marketplace_settings.is_marketplace_enabled"
	}).then(r => r.message)
}
