import click


def execute():

	click.secho(
		"Agriculture Domain is moved to a separate app and will be removed from CapKPI in version-14.\n"
		"Please install the app to continue using the Agriculture domain: https://github.com/FINERGYRS/agriculture",
		fg="yellow",
	)
