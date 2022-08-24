finergy.provide('capkpi.PointOfSale');

finergy.pages['point-of-sale'].on_page_load = function(wrapper) {
	finergy.ui.make_app_page({
		parent: wrapper,
		title: __('Point of Sale'),
		single_column: true
	});

	finergy.require('point-of-sale.bundle.js', function() {
		wrapper.pos = new capkpi.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	});
};

finergy.pages['point-of-sale'].refresh = function(wrapper) {
	if (document.scannerDetectionData) {
		onScan.detachFrom(document);
		wrapper.pos.wrapper.html("");
		wrapper.pos.check_opening_entry();
	}
};
