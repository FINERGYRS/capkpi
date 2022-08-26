import click
import finergy


def execute():
	if not finergy.db.exists("Company", {"country": "India"}):
		return

	click.secho(
		"India-specific regional features have been moved to a separate app"
		" and will be removed from CapKPI in Version 14."
		" Please install India Compliance after upgrading to Version 14:\n"
		"https://github.com/resilient-tech/india-compliance",
		fg="yellow",
	)
