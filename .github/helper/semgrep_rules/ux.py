import finergy
from finergy import _, msgprint, throw

# ruleid: finergy-missing-translate-function-python
throw("Error Occured")

# ruleid: finergy-missing-translate-function-python
finergy.throw("Error Occured")

# ruleid: finergy-missing-translate-function-python
finergy.msgprint("Useful message")

# ruleid: finergy-missing-translate-function-python
msgprint("Useful message")


# ok: finergy-missing-translate-function-python
translatedmessage = _("Hello")

# ok: finergy-missing-translate-function-python
throw(translatedmessage)

# ok: finergy-missing-translate-function-python
msgprint(translatedmessage)

# ok: finergy-missing-translate-function-python
msgprint(_("Helpful message"))

# ok: finergy-missing-translate-function-python
finergy.throw(_("Error occured"))
