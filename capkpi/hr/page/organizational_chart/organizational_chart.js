finergy.pages['organizational-chart'].on_page_load = function(wrapper) {
	finergy.ui.make_app_page({
		parent: wrapper,
		title: __('Organizational Chart'),
		single_column: true
	});

	$(wrapper).bind('show', () => {
		finergy.require('/assets/js/hierarchy-chart.min.js', () => {
			let organizational_chart = undefined;
			let method = 'capkpi.hr.page.organizational_chart.organizational_chart.get_children';

			if (finergy.is_mobile()) {
				organizational_chart = new capkpi.HierarchyChartMobile('Employee', wrapper, method);
			} else {
				organizational_chart = new capkpi.HierarchyChart('Employee', wrapper, method);
			}

			finergy.breadcrumbs.add('HR');
			organizational_chart.show();
		});
	});
};
