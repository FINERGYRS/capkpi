import click


def execute():

	click.secho(
		"Education Domain is moved to a separate app and will be removed from CapKPI in version-14.\n"
		"When upgrading to CapKPI version-14, please install the app to continue using the Education domain: https://github.com/finergyrs/education",
		fg="yellow",
	)
