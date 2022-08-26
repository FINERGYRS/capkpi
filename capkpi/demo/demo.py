import sys

import finergy
import finergy.utils

import capkpi
from capkpi.demo.setup import education, healthcare, manufacture, retail, setup_data
from capkpi.demo.user import accounts
from capkpi.demo.user import education as edu
from capkpi.demo.user import fixed_asset, hr, manufacturing, projects, purchase, sales, stock

"""
Make a demo

1. Start with a fresh account

bench --site demo.capkpi.dev reinstall

2. Install Demo

bench --site demo.capkpi.dev execute capkpi.demo.demo.make

3. If Demo breaks, to continue

bench --site demo.capkpi.dev execute capkpi.demo.demo.simulate

"""


def make(domain="Manufacturing", days=100):
	finergy.flags.domain = domain
	finergy.flags.mute_emails = True
	setup_data.setup(domain)
	if domain == "Manufacturing":
		manufacture.setup_data()
	elif domain == "Retail":
		retail.setup_data()
	elif domain == "Education":
		education.setup_data()
	elif domain == "Healthcare":
		healthcare.setup_data()

	site = finergy.local.site
	finergy.destroy()
	finergy.init(site)
	finergy.connect()

	simulate(domain, days)


def simulate(domain="Manufacturing", days=100):
	runs_for = finergy.flags.runs_for or days
	finergy.flags.company = capkpi.get_default_company()
	finergy.flags.mute_emails = True

	if not finergy.flags.start_date:
		# start date = 100 days back
		finergy.flags.start_date = finergy.utils.add_days(finergy.utils.nowdate(), -1 * runs_for)

	current_date = finergy.utils.getdate(finergy.flags.start_date)

	# continue?
	demo_last_date = finergy.db.get_global("demo_last_date")
	if demo_last_date:
		current_date = finergy.utils.add_days(finergy.utils.getdate(demo_last_date), 1)

	# run till today
	if not runs_for:
		runs_for = finergy.utils.date_diff(finergy.utils.nowdate(), current_date)
		# runs_for = 100

	fixed_asset.work()
	for i in range(runs_for):
		sys.stdout.write("\rSimulating {0}: Day {1}".format(current_date.strftime("%Y-%m-%d"), i))
		sys.stdout.flush()
		finergy.flags.current_date = current_date
		if current_date.weekday() in (5, 6):
			current_date = finergy.utils.add_days(current_date, 1)
			continue
		try:
			hr.work()
			purchase.work()
			stock.work()
			accounts.work()
			projects.run_projects(current_date)
			sales.work(domain)
			# run_messages()

			if domain == "Manufacturing":
				manufacturing.work()
			elif domain == "Education":
				edu.work()

		except Exception:
			finergy.db.set_global("demo_last_date", current_date)
			raise
		finally:
			current_date = finergy.utils.add_days(current_date, 1)
			finergy.db.commit()
