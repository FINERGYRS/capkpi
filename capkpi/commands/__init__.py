# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# GPL v3 License. See license.txt

import click


def call_command(cmd, context):
	return click.Context(cmd, obj=context).forward(cmd)


commands = []
